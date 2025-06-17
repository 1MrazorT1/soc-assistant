import cupy
print("CuPy imported from:", cupy.__file__)
print("CUDA runtime:", cupy.cuda.runtime.runtimeGetVersion())