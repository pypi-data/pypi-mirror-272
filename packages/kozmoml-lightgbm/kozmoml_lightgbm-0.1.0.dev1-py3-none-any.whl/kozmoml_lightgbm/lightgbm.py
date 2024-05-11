import lightgbm as lgb

from kozmoml import types
from kozmoml.model import MLModel
from kozmoml.utils import get_model_uri
from kozmoml.codecs import NumpyCodec, NumpyRequestCodec


WELLKNOWN_MODEL_FILENAMES = ["model.bst"]


class LightGBMModel(MLModel):
    """
    Implementationof the MLModel interface to load and serve `lightgbm` models.
    """

    async def load(self) -> bool:
        model_uri = await get_model_uri(
            self._settings, wellknown_filenames=WELLKNOWN_MODEL_FILENAMES
        )

        self._model = lgb.Booster(model_file=model_uri)

        return True

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        decoded = self.decode_request(payload, default_codec=NumpyRequestCodec)
        prediction = self._model.predict(decoded)

        return types.InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=[
                NumpyCodec.encode_output(
                    name="predict", payload=prediction  # type: ignore
                )
            ],
        )
