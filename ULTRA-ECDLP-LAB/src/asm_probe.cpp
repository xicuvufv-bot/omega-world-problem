// asm_probe.cpp — compile with -S to inspect hot functions individually.
// Each function is marked noinline and forced alive so its body survives in .s.
#include <cstdint>
#include "instance.hpp"
#include "src/fp.hpp"
#include "src/ec.hpp"

template <typename F>
__attribute__((noinline)) uint32_t probe_mul(uint32_t a, uint32_t b) {
    return (uint32_t)F::mul(a, b);
}
template <typename F>
__attribute__((noinline)) uint32_t probe_sub(uint32_t a, uint32_t b) {
    return (uint32_t)F::sub(a, b);
}
template <typename F>
__attribute__((noinline)) uint32_t probe_inv(uint32_t a) {
    return (uint32_t)F::inv(a);
}

template <typename F>
__attribute__((noinline)) ec::Jacobian<F> probe_jdbl(ec::Jacobian<F> p) {
    return ec::Jacobian<F>::dbl(p);
}
template <typename F>
__attribute__((noinline)) ec::Jacobian<F> probe_jadd(ec::Jacobian<F> a, ec::Jacobian<F> b) {
    return ec::Jacobian<F>::add(a, b);
}
template <typename F>
__attribute__((noinline)) ec::Jacobian<F> probe_jmixed(ec::Jacobian<F> a, ec::Affine<F> b) {
    return ec::Jacobian<F>::add_affine(a, b);
}

using N = fp::FpNaive<TOY_P>;
using B = fp::FpBarrett<TOY_P>;
using M = fp::FpMont<TOY_P>;
using Q = fp::FpPseudo<TOY_P>;
using JN = ec::Jacobian<N>;
using JB = ec::Jacobian<B>;
using JM = ec::Jacobian<M>;
using JQ = ec::Jacobian<Q>;

uint32_t test_mul(uint32_t a, uint32_t b) { return probe_mul<N>(a,b); }
extern "C" uint32_t test_inv(uint32_t a) { return probe_inv<N>(a); }
extern "C" JN test_jdbl(JN p) { return probe_jdbl<N>(p); }

template uint32_t probe_mul<N>(uint32_t, uint32_t);
template uint32_t probe_mul<B>(uint32_t, uint32_t);
template uint32_t probe_mul<M>(uint32_t, uint32_t);
template uint32_t probe_mul<Q>(uint32_t, uint32_t);
template uint32_t probe_sub<Q>(uint32_t, uint32_t);
template uint32_t probe_inv<N>(uint32_t);
template uint32_t probe_inv<M>(uint32_t);
template JN probe_jdbl<N>(JN);
template JN probe_jadd<N>(JN, JN);
template JN probe_jmixed<N>(JN, ec::Affine<N>);
template JB probe_jdbl<B>(JB);
template JM probe_jdbl<M>(JM);
template JQ probe_jdbl<Q>(JQ);