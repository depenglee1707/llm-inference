from abc import ABC, abstractmethod
from typing import List, Optional, Any
from ray.air import ScalingConfig
from ray.util.placement_group import PlacementGroup
from llmserve.backend.server.models import Prompt

from llmserve.backend.logger import get_logger

from typing import List, Optional
from ray.air import ScalingConfig

from llmserve.backend.logger import get_logger
from llmserve.backend.server.models import Args, Prompt
import asyncio
from typing import AsyncGenerator, Generator

logger = get_logger(__name__)

class LLMEngine(ABC):
    args: Args = None
    """Initialize model and tokenizer and place them on the correct device.

    Args:
        device (torch.device): Device to place model and tokenizer on.
        world_size (int): Number of GPUs to use.
    """

    def __init__(
        self,
        args: Args,

    ):
        self.args = args

    @abstractmethod
    async def launch_engine(
            self, 
            scaling_config: ScalingConfig,
            placement_group: PlacementGroup,
            scaling_options: dict,
        ) -> Any:
        """Load model.

        Args:
            model_id (str): Hugging Face model ID.
        """
        pass

    @abstractmethod
    async def predict(
            self,
            prompts: List[Prompt],
            *,
            timeout_s: float = 60,
            start_timestamp: Optional[float] = None,
            lock: asyncio.Lock,
        ) -> List[str]:
        """Load model.

        Args:
            model_id (str): Hugging Face model ID.
        """
        pass
    
    @abstractmethod
    async def check_health(self):
        pass
    
    @abstractmethod
    def stream_generate_texts(self, prompt: str) -> Generator[str, None, None]:
        pass