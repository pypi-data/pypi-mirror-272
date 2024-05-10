import logging
import math
from datetime import datetime
from datetime import timezone
import numpy as np
import json
import queue
import threading
import asyncio


class TrainUtils:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.indraserver_profile = None
        self.indra_active = False
        self.icl = None
        self.train_session_active = False
        self.session_id = None

    async def init_indra(self, indraserver_profile, username=None, password=None):
        self.indraserver_profile = None
        self.indra_active = False
        self.icl = None
        self.session_id = None
        if indraserver_profile is not None:
            self.indraserver_profile = indraserver_profile
            try:
                from indralib.indra_client import IndraClient
            except Exception as e:
                self.log.error(
                    f"indralib is required to use the indraserver_profile: {e}"
                )
                self.indraserver_profile = None
        else:
            self.log.error("No indraserver_profile provided")
            return False
        if self.indraserver_profile is not None:
            self.icl = IndraClient(verbose=False, profile="default")
        if self.icl is None:
            logging.error("Could not create Indrajala client")
            return False
        ws = await self.icl.init_connection(verbose=False)
        if ws is None:
            logging.error("Could not connect to Indrajala")
            self.indraserver_profile = None
            return False
        else:
            self.indra_active = True
            self.log.info(f"Connected to Indrajala server {indraserver_profile}")
            if username is not None and password is not None:
                self.session_id = await self.icl.login_wait(username, password)
                if self.session_id is None:
                    self.log.error("Could not log in to Indrajala")
                    self.indra_active = False
                    return False
                else:
                    self.log.info(
                        f"Logged in to Indrajala as {username}, session {self.session_id}"
                    )
                    return True
            else:
                self.log.error("No username and password provided")
                return False

    @staticmethod
    def progress_bar_string(progress, max_progress, bar_length=20):
        """Create a Unicode progress bar string

        This creates a string of length bar_length with a Unicode progress bar using
        fractional Unicode block characters. The returned string is always of constant
        length and is suitable for printing to a terminal or notebook.

        This pretty much obsoletes the `tqdm` or similar package for simple progress bars.

        :param progress: current progress
        :param max_progress: maximum progress
        :param bar_length: length of the progress bar
        :return: Unicode progress bar string of length `bar_length`
        """
        progress_frac = progress / max_progress
        num_blocks = int(bar_length * progress_frac)
        rem = bar_length * progress_frac - num_blocks
        blocks = " ▏▎▍▌▋▊▉█"
        remainder_index = int(rem * len(blocks))
        bar = blocks[-1] * num_blocks
        if remainder_index > 0:
            bar += blocks[remainder_index]
        bar += " " * (bar_length - len(bar))
        return bar

    def train_session_start(
        self,
        model_name,
        model_description,
        model_version,
        model_params,
        indra_subdomain=None,
    ):
        if self.train_session_active is True:
            self.log.warning(
                "Training session already active, closing existing session"
            )
            self.train_session_end()
        self.model_name = model_name
        self.model_description = model_description
        self.model_version = model_version
        self.model_params = model_params
        if indra_subdomain is None:
            subdomain = f"{model_name}/{model_version}".replace(" ", "_")
            self.log.warning(f"No Indrajala subdomain set, using {subdomain}")
        self.indra_subdomain = indra_subdomain
        self.model_loss_history = []
        self.losses = np.array([])

        self.indra_queue = queue.Queue()
        self.indra_thread_running = True
        self.sync_indra = threading.Thread(
            target=self.sync_logger_worker,
            name="_sync_logger_worker",
            args=[],
            daemon=True,
        )
        self.sync_indra.start()

        self.train_session_active = True

    def sync_logger_worker(self):
        self.log.info("Starting indra thread")
        while self.indra_thread_running is True:
            try:
                rec = self.indra_queue.get(timeout=0.01)
            except queue.Empty:
                continue
            asyncio.run(self.register_train_state(rec))
            self.indra_queue.task_done()
        self.log.info("Stopped indra thread")

    def train_session_end(self):
        self.indra_thread_running = False
        if not self.train_session_active:
            self.log.error(
                "No active training session: use train_session_start() first"
            )
            return
        self.train_session_active = False

    async def indra_report(self, record):
        if not self.indra_active:
            self.log.error("Indrajala not active")
            return
        from indralib.indra_event import IndraEvent

        event = IndraEvent()
        event.domain = f"$event/ml/model/train/{self.indra_subdomain}/record"
        event.from_id = "python/ml_indie_tools"
        event.to_scope = "public"
        event.data_type = "json/ml/trainrecord"
        event.data = json.dumps(record)
        event.auth_hash = self.session_id
        await self.icl.send_event(event)

        event = IndraEvent()
        event.domain = f"$event/ml/model/train/{self.indra_subdomain}/loss"
        event.from_id = "python/ml_indie_tools"
        event.to_scope = "public"
        event.data_type = "number/float"
        event.data = json.dumps(record["mean_loss"])
        event.auth_hash = self.session_id
        await self.icl.send_event(event)

    def train_state(
        self,
        current_epoch,
        current_batch,
        num_batches,
        loss,
        val_loss=None,
        mean_loss_window=20,
    ):
        if self.train_session_active is False:
            self.log.error(
                "No active training session at train_state(): use train_session_start() first"
            )
            return "n/a"
        # Calculate perplexity, accuracy from loss:
        perplexity = math.exp(loss)
        if val_loss is not None:
            val_perplexity = math.exp(val_loss)
        else:
            val_perplexity = None
        accuracy = 1 - loss
        if val_loss is not None:
            val_accuracy = 1 - val_loss
        else:
            val_accuracy = None
        self.losses = np.append(self.losses, loss)
        mean_loss = np.mean(self.losses[-mean_loss_window:])
        record = {
            "epoch": current_epoch,
            "loss": loss,
            "mean_loss": mean_loss,
            "perplexity": perplexity,
            "accuracy": accuracy,
            "val_loss": val_loss,
            "val_perplexity": val_perplexity,
            "val_accuracy": val_accuracy,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.model_loss_history.append(record)

        if self.indra_active:
            self.indra_queue.put(record)

        pbar = self.progress_bar_string(current_batch, num_batches)

        status_string = f"{current_batch:6d} ⦊{pbar}⦉ loss: {mean_loss:.4f}    "
        return status_string, record

    async def register_train_state(self, record):
        if self.indra_active:
            await self.indra_report(record)
