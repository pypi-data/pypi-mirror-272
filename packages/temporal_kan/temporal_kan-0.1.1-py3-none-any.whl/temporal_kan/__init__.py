from temporal_kan.spline import power_spline
from temporal_kan.sr import SRKAN
from temporal_kan.gr import GRKAN
from temporal_kan.sltsm import SLSTM_KAN
from temporal_kan.glstm import GLSTM_KAN


def TemporalKanModel(model_type: str = 'SRKAN', *args, **kwargs):
    if model_type == 'SRKAN':
        return SRKAN(*args, **kwargs)
    elif model_type == 'GRKAN':
        return GRKAN(*args, **kwargs)
    elif model_type == 'SLSTM_KAN':
        return SLSTM_KAN(*args, **kwargs)
    elif model_type == 'GLSTM_KAN':
        return GLSTM_KAN(*args, **kwargs)
    else:
        raise ValueError('Invalid model type')