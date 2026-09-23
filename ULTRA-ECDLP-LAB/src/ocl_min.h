// ocl_min.h — minimal OpenCL 1.2/2.x declarations for MinGW (no system CL header present).
// Covers only what gpu_main.cpp uses: platform/device/context/queue/program/kernel/buffer.
#pragma once
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef int32_t   cl_int;
typedef uint32_t  cl_uint;
typedef uint64_t  cl_ulong;
typedef uint32_t  cl_bool;
typedef intptr_t  cl_context_properties;
typedef intptr_t  cl_platform_id;
typedef cl_uint   cl_bitfield;
typedef cl_bitfield cl_device_type;
typedef cl_uint   cl_mem_flags;
typedef cl_bitfield cl_command_queue_properties;
typedef cl_uint   cl_profiling_info;
typedef cl_uint   cl_device_info;
typedef cl_uint   cl_program_build_info;
typedef cl_uint   cl_kernel_work_group_info;
typedef cl_uint   cl_platform_info;
typedef cl_uint   cl_context_info;
typedef cl_uint   cl_event_info;
typedef intptr_t  cl_context;
typedef intptr_t  cl_device_id;
typedef intptr_t  cl_command_queue;
typedef intptr_t  cl_mem;
typedef intptr_t  cl_program;
typedef intptr_t  cl_kernel;
typedef intptr_t  cl_event;

#define CL_SUCCESS                        0
#define CL_DEVICE_TYPE_GPU                (1 << 2)
#define CL_DEVICE_TYPE_ALL                0xFFFFFFFF
#define CL_PLATFORM_NAME                  0x0902
#define CL_PLATFORM_VERSION               0x0901
#define CL_DEVICE_NAME                    0x102B
#define CL_DEVICE_MAX_COMPUTE_UNITS       0x1002
#define CL_DEVICE_MAX_CLOCK_FREQUENCY     0x100C
#define CL_DEVICE_MAX_WORK_GROUP_SIZE     0x1004
#define CL_DEVICE_GLOBAL_MEM_SIZE         0x101F
#define CL_DEVICE_LOCAL_MEM_SIZE          0x1023
#define CL_MEM_READ_WRITE                 (1 << 0)
#define CL_MEM_COPY_HOST_PTR              (1 << 5)
#define CL_MEM_HOST_READ_ONLY             (1 << 4)
#define CL_TRUE                           1
#define CL_FALSE                          0
#define CL_PROGRAM_BUILD_LOG              0x1183
#define CL_PROFILING_COMMAND_START        0x1282
#define CL_PROFILING_COMMAND_END          0x1283
#define CL_KERNEL_WORK_GROUP_SIZE         0x11B0
#define CL_QUEUE_PROFILING_ENABLE         (1 << 1)

cl_int clGetPlatformIDs(cl_uint, cl_platform_id*, cl_platform_id*);
cl_int clGetPlatformInfo(cl_platform_id, cl_platform_info, size_t, void*, size_t*);
cl_int clGetDeviceIDs(cl_platform_id, cl_device_type, cl_uint, cl_device_id*, cl_uint*);
cl_int clGetDeviceInfo(cl_device_id, cl_device_info, size_t, void*, size_t*);
cl_context clCreateContext(const cl_context_properties*, cl_uint, const cl_device_id*,
                           void (*)(const char*, const void*, size_t, void*),
                           void*, cl_int*);
cl_command_queue clCreateCommandQueue(cl_context, cl_device_id, cl_command_queue_properties, cl_int*);
cl_program clCreateProgramWithSource(cl_context, cl_uint, const char**, const size_t*, cl_int*);
cl_int clBuildProgram(cl_program, cl_uint, const cl_device_id*, const char*,
                      void (*)(cl_program, void*), void*);
cl_int clGetProgramBuildInfo(cl_program, cl_device_id, cl_program_build_info,
                             size_t, void*, size_t*);
cl_kernel clCreateKernel(cl_program, const char*, cl_int*);
cl_int clSetKernelArg(cl_kernel, cl_uint, size_t, const void*);
cl_mem clCreateBuffer(cl_context, cl_mem_flags, size_t, void*, cl_int*);
cl_int clEnqueueNDRangeKernel(cl_command_queue, cl_kernel, cl_uint,
                              const size_t*, const size_t*, const size_t*,
                              cl_uint, const cl_event*, cl_event*);
cl_int clEnqueueReadBuffer(cl_command_queue, cl_mem, cl_bool, size_t, size_t, void*,
                           cl_uint, const cl_event*, cl_event*);
cl_int clEnqueueWriteBuffer(cl_command_queue, cl_mem, cl_bool, size_t, size_t, const void*,
                            cl_uint, const cl_event*, cl_event*);
cl_int clFinish(cl_command_queue);
cl_int clFlush(cl_command_queue);
cl_int clGetKernelWorkGroupInfo(cl_kernel, cl_device_id, cl_kernel_work_group_info,
                                size_t, void*, size_t*);
cl_int clReleaseMemObject(cl_mem);
cl_int clReleaseKernel(cl_kernel);
cl_int clReleaseProgram(cl_program);
cl_int clReleaseCommandQueue(cl_command_queue);
cl_int clReleaseContext(cl_context);

#ifdef __cplusplus
}
#endif
