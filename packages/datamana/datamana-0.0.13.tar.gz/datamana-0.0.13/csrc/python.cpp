#include <nanobind/nanobind.h>
#include "semaphore.hpp"
#include "mqueue.hpp"
#include "shared_memory.hpp"

namespace nb = nanobind;

NB_MODULE(_C, m) {
    DEFINE_SEMAPHORE_MODULE(m);
    DEFINE_MQUEUE_MODULE(m);
    DEFINE_SHAREDMEMORY_MODULE(m);
}
