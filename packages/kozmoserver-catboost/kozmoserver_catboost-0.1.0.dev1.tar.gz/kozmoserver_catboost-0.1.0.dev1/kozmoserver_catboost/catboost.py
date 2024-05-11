from catboost import CatBoostClassifier

from kozmoserver import types
from kozmoserver.model import MLModel
from kozmoserver.utils import get_model_uri
from kozmoserver.codecs import NumpyCodec, NumpyRequestCodec


WELLKNOWN_MODEL_FILENAMES = ["model.cbm", "model.bin"]


class CatboostModel(MLModel):
    """
    Implementation of the MLModel interface to load and serve `catboost` models.
    """

    async def load(self) -> bool:
        model_uri = await get_model_uri(
            self._settings, wellknown_filenames=WELLKNOWN_MODEL_FILENAMES
        )

        self._model = CatBoostClassifier()
        self._model.load_model(model_uri)
        self.ready = True
        return self.ready

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        decoded = self.decode_request(payload, default_codec=NumpyRequestCodec)
        prediction = self._model.predict(decoded)

        return types.InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=[NumpyCodec.encode(name="predict", payload=prediction)],
        )
