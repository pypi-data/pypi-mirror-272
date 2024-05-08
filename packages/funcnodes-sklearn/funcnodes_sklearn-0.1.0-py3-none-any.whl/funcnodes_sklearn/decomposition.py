from funcnodes import Shelf, NodeDecorator
from exposedfunctionality import controlled_wrapper
from typing import Literal, Optional, Union, Callable
import numpy as np
from sklearn.base import BaseEstimator
from enum import Enum
from sklearn.decomposition import (
    DictionaryLearning,
    FactorAnalysis,
    FastICA,
    IncrementalPCA,
    KernelPCA,
    LatentDirichletAllocation,
    MiniBatchDictionaryLearning,
    MiniBatchSparsePCA,
    NMF,
    MiniBatchNMF,
    PCA,
    SparsePCA,
    SparseCoder,
    TruncatedSVD,
)

class FitAlgorithm(Enum):
    lars = "lars"
    cd = "cd"
    
    @classmethod
    def default(cls):
        return cls.lars.value
    
    
class TransformAlgorithm(Enum):
    lasso_lars = "lasso_lars"
    lasso_cd = "lasso_cd"
    lars = "lars"
    omp = "omp"
    threshold = "threshold"
    
    @classmethod
    def default(cls):
        return cls.omp.value
   
@NodeDecorator(
    node_id = "DictionaryLearning",
    name="DictionaryLearning",
)
@controlled_wrapper(DictionaryLearning, wrapper_attribute="__fnwrapped__")
def _dictionary_learning(
    n_components: Optional[int] = None,
    alpha: float = 1.0,
    max_iter: int = 1000,
    tol: float = 1e-8,
    fit_algorithm: FitAlgorithm = FitAlgorithm.default(),
    transform_algorithm: TransformAlgorithm = TransformAlgorithm.default(),
    transform_n_nonzero_coefs: Optional[int] = None,
    transform_alpha: Optional[float] = None,
    n_jobs: Optional[int] = None,
    code_init: Optional[np.ndarray] = None,
    dict_init: Optional[np.ndarray] = None,
    callback: Optional[Callable] = None,
    verbose: bool = False,
    split_sign: bool = False,
    random_state: Optional[Union[int, np.random.RandomState]] = None,
    positive_code: bool = False,
    positive_dict: bool = False,
    transform_max_iter: int = 1000,
) -> BaseEstimator:

    def create_dictionary_learning():
        return DictionaryLearning(
            n_components=n_components,
            alpha=alpha,
            max_iter=max_iter,
            tol=tol,
            fit_algorithm=fit_algorithm,
            transform_algorithm=transform_algorithm,
            transform_n_nonzero_coefs=transform_n_nonzero_coefs,
            transform_alpha=transform_alpha,
            n_jobs=n_jobs,
            code_init=code_init,
            dict_init=dict_init,
            callback=callback,
            verbose=verbose,
            split_sign=split_sign,
            random_state=random_state,
            positive_code=positive_code,
            positive_dict=positive_dict,
            transform_max_iter=transform_max_iter
        )
    return create_dictionary_learning()


class SVDMethod(Enum):
    lapack = "lapack"
    randomized = "randomized"
    
    @classmethod
    def default(cls):
        return cls.randomized.value


class Rotation(Enum):
    varimax = "varimax"
    quartimax = "quartimax"
    NONE = None
    
    @classmethod
    def default(cls):
        return cls.NONE.value
    
    
@NodeDecorator(
    node_id = "FactorAnalysis",
    name="FactorAnalysis",
)
@controlled_wrapper(FactorAnalysis, wrapper_attribute="__fnwrapped__")
def _factor_analysis(
    n_components: Optional[int] = None,
    tol: float = 1e-2,
    copy: bool = True,
    max_iter: int = 1000,
    noise_variance_init: Optional[np.ndarray] = None,
    svd_method: SVDMethod = SVDMethod.default(),
    iterated_power: int = 3,
    rotation: Rotation = Rotation.default(),
    random_state: Optional[Union[int, np.random.RandomState]] = 0,
) -> BaseEstimator:

    def create_factor_analysis():
        return FactorAnalysis(
            n_components=n_components,
            copy=copy,
            max_iter=max_iter,
            tol=tol,
            noise_variance_init=noise_variance_init,
            svd_method=svd_method,
            iterated_power=iterated_power,
            rotation=rotation,
            random_state=random_state,
        )
    return create_factor_analysis()



class Algorithm(Enum):
    parallel = "parallel"
    deflation = "deflation"
    
    @classmethod
    def default(cls):
        return cls.parallel.value
   
class Fun(Enum):
    logcosh = "logcosh"
    exp = "exp"
    cube = "cube"
    
    @classmethod
    def default(cls):
        return cls.logcosh.value
    
class WhitenSolver(Enum):
    eigh = "eigh"
    svd = "svd"
    
    @classmethod
    def default(cls):
        return cls.svd.value
    
@NodeDecorator(
    node_id = "FastICA",
    name="FastICA",
)
@controlled_wrapper(FastICA, wrapper_attribute="__fnwrapped__")
def _fast_ica(
    n_components: Optional[int] = None,
    algorithm: Algorithm = Algorithm.default(),
    fun: Optional[Union[Fun, Callable]] = Fun.default(),
    fun_args: Optional[dict] = None,
    max_iter: int = 200,
    tol: float = 1e-4,
    w_init: Optional[np.ndarray] = None,
    whiten_solver: WhitenSolver = WhitenSolver.default(),
    random_state: Optional[Union[int, np.random.RandomState]] = None,
) -> BaseEstimator:

    def create_fast_ica():
        return FastICA(
            n_components=n_components,
            algorithm=algorithm,
            max_iter=max_iter,
            tol=tol,
            fun=fun,
            fun_args=fun_args,
            w_init=w_init,
            whiten_solver=whiten_solver,
            random_state=random_state,
        )
    return create_fast_ica()


@NodeDecorator(
    node_id = "IncrementalPCA",
    name="IncrementalPCA",
)
@controlled_wrapper(IncrementalPCA, wrapper_attribute="__fnwrapped__")
def _incrementa_lpca(
    n_components: Optional[int] = None,
    whiten: bool = False,
    copy: bool = True,
    batch_size: Optional[int] = None,
) -> BaseEstimator:

    def create_incrementa_lpca():
        return IncrementalPCA(
            n_components=n_components,
            whiten=whiten,
            batch_size=batch_size,
            copy=copy,
        )
    return create_incrementa_lpca()

class Kernel(Enum):
    linear = "linear"
    poly = "poly"
    rbf = "rbf"
    sigmoid = "sigmoid"
    cosine = "cosine"
    precomputed = "precomputed"
    
    @classmethod
    def default(cls):
        return cls.linear.value

class EigenSolvers(Enum):
    auto = "auto"
    dense = "dense"
    arpack = "arpack"
    randomized = "randomized"
    
    @classmethod
    def default(cls):
        return cls.auto.value
    
    
@NodeDecorator(
    node_id = "KernelPCA",
    name="KernelPCA",
)
@controlled_wrapper(KernelPCA, wrapper_attribute="__fnwrapped__")
def _kernel_lpca(
    n_components: Optional[int] = None,
    kernel: Optional[Union[Kernel, Callable]] = Kernel.default(),
    gamma: Optional[float] = None,
    degree:int = 3,
    coef0: float = 1,
    kernel_params: Optional[dict] = None,
    alpha: float = 1.0,
    fit_inverse_transform: bool = False,
    eigen_solver: EigenSolvers = EigenSolvers.default(),
    tol: float = 0.0,
    max_iter: Optional[int] = None,
    iterated_power: Optional[Union[int, Literal["auto"]]] = "auto",
    remove_zero_eig: bool = False,
    random_state: Optional[Union[int, np.random.RandomState]] = None,
    copy_X: bool = True,
    n_jobs: Optional[int] = None,
) -> BaseEstimator:

    def create_kernel_lpca():
        return KernelPCA(
            n_components=n_components,
            kernel=kernel,
            max_iter=max_iter,
            tol=tol,
            degree=degree,
            gamma=gamma,
            coef0=coef0,
            kernel_params=kernel_params,
            alpha=alpha,
            fit_inverse_transform=fit_inverse_transform,
            eigen_solver=eigen_solver,
            iterated_power=iterated_power,
            remove_zero_eig=remove_zero_eig,
            copy_X=copy_X,
            n_jobs=n_jobs,
            random_state=random_state,
        )
    return create_kernel_lpca()



CROSS_DECOMPOSITION_NODE_SHELFE = Shelf(
    nodes=[
        _dictionary_learning,
        _factor_analysis,
        _fast_ica,
        _incrementa_lpca,
        _kernel_lpca,
        
    ],
    subshelves=[],
    name="Matrix Decomposition",
    description="The sklearn.decomposition module includes matrix decomposition algorithms, including among others PCA, NMF or ICA. Most of the algorithms of this module can be regarded as dimensionality reduction techniques.",
)
