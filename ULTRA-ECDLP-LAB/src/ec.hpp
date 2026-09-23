// ec.hpp — elliptic curve y^2 = x^3 + 7 over a toy field (templates over field type)
// Coordinate systems compared experimentally: affine, Jacobian, mixed (Jacobian + affine).
// Operation counters attached (M = field mult, S = square, I = inverse) — verified empirically.
#pragma once
#include "fp.hpp"

namespace ec {

template <typename F>
struct Affine {
    using Elem = typename F::Elem;
    Elem x, y;
    bool inf;

    static Affine zero() { Affine a; a.x = F::zero(); a.y = F::zero(); a.inf = true; return a; }
    static Affine point(Elem X, Elem Y) { Affine a; a.x = F::from_raw(X); a.y = F::from_raw(Y); a.inf = false; return a; }
    static Affine rep(Elem X, Elem Y) { Affine a; a.x = X; a.y = Y; a.inf = false; return a; }
    bool is_zero() const { return inf; }

    // A + B : slope = (yB-yA)/(xB-xA)   (8M+1I typical, we count: 2 sub-free, 1 inv, 2 mul, 1 sqr)
    // cost: 1I + 3M + 1S
    static Affine add(const Affine& a, const Affine& b) {
        if (a.is_zero()) return b;
        if (b.is_zero()) return a;
        // dbl case
        if (a.x == b.x) {
            if (a.y == b.y) return dbl(a);
            return zero();
        }
        Elem dx = F::sub(b.x, a.x);
        Elem dy = F::sub(b.y, a.y);
        Elem m  = F::mul(dy, F::inv(dx));                       // 1I + 1M
        Elem x3 = F::sub(F::sub(F::sqr(m), a.x), b.x);          // 1S
        Elem y3 = F::sub(F::mul(m, F::sub(a.x, x3)), a.y);      // 1M
        return rep(x3, y3);
    }
    static Affine dbl(const Affine& a) {
        if (a.is_zero()) return a;
        // slope = 3x^2/(2y)  ; for y^2=x^3+B : 3x^2+?  B doesn't matter (d/dx)
        Elem xx = F::sqr(a.x);                                   // 1S
        Elem num = F::add(F::add(xx, xx), xx);                   // 3x^2
        Elem twoy = F::add(a.y, a.y);
        Elem m = F::mul(num, F::inv(twoy));                      // 1I + 1M
        Elem x3 = F::sub(F::sqr(m), F::add(a.x, a.x));           // 1S
        Elem y3 = F::sub(F::mul(m, F::sub(a.x, x3)), a.y);       // 1M
        return rep(x3, y3);
    }
    // scalar mult — double-and-add always-add (constant schedule, for benchmarking)
    static Affine mul(const Affine& p, uint64_t k) {
        Affine r = zero();
        Affine b = p;
        while (k) {
            if (k & 1) r = add(r, b);
            b = dbl(b);
            k >>= 1;
        }
        return r;
    }
};

// Jacobian: (X,Y,Z) -> affine (X/Z^2, Y/Z^3), Z=0 encodes infinity
template <typename F>
struct Jacobian {
    using Elem = typename F::Elem;
    Elem X, Y, Z;
    bool inf;

    static Jacobian zero() { Jacobian j; j.X=F::zero(); j.Y=F::zero(); j.Z=F::zero(); j.inf=true; return j; }
    static Jacobian from_affine_xz(Elem Xn, Elem Yn, Elem Zn) { Jacobian j; j.X=Xn; j.Y=Yn; j.Z=Zn; j.inf=false; return j; }
    static Jacobian from_affine(Elem x, Elem y) { return from_affine_xz(F::from_raw(x), F::from_raw(y), F::one()); }
    bool is_zero() const { return inf; }

    // a=0 doubling (y^2=x^3+B): 4M+6S
    //   S = 4*X*Y^2 ; M = 3*X^2 ; X3 = M^2-2S ; Y3 = M(S-X3)-8Y^4 ; Z3 = 2YZ
    static Jacobian dbl(const Jacobian& p) {
        if (p.is_zero()) return p;
        Elem XX = F::sqr(p.X);                                   // S
        Elem YY = F::sqr(p.Y);                                   // S
        Elem YY2 = F::add(YY, YY);                               // 2Y^2
        Elem S  = F::add(F::mul(p.X, YY2), F::mul(p.X, YY2));    // 2M : S = 4XY^2
        Elem M  = F::add(XX, F::add(XX, XX));                    // 3X^2
        Elem X3 = F::sub(F::sqr(M), F::add(S, S));               // S
        Elem Z3 = F::mul(F::add(p.Z, p.Z), p.Y);                 // M : Z3 = 2YZ
        Elem YY4 = F::sqr(YY);                                   // S : Y4 = Y^4
        Elem y8 = F::add(F::add(YY4, YY4), F::add(YY4, YY4));    // 4Y^4
        y8 = F::add(y8, y8);                                     // 8Y^4
        Elem Y3 = F::sub(F::mul(M, F::sub(S, X3)), y8);          // M : M(S-X3) - 8Y^4
        return from_affine_xz(X3, Y3, Z3);
    }

    // full add (a != b, both nz): 12M+4S
    static Jacobian add(const Jacobian& a, const Jacobian& b) {
        if (a.is_zero()) return b;
        if (b.is_zero()) return a;
        Elem Z1Z1 = F::sqr(a.Z);          // S
        Elem Z2Z2 = F::sqr(b.Z);          // S
        Elem U1 = F::mul(a.X, Z2Z2);      // M
        Elem U2 = F::mul(b.X, Z1Z1);      // M
        Elem S1 = F::mul(a.Y, F::mul(Z2Z2, b.Z)); // M*M = 2M
        Elem S2 = F::mul(b.Y, F::mul(Z1Z1, a.Z)); // 2M
        if (U1 == U2) {
            if (S1 == S2) return dbl(a);
            return zero();
        }
        Elem H = F::sub(U2, U1);          // 
        Elem R = F::sub(S2, S1);          //
        Elem HH = F::sqr(H);              // S
        Elem HHH = F::mul(H, HH);         // M
        Elem V = F::mul(U1, HH);          // M
        Elem X3 = F::sub(F::sub(F::sqr(R), HHH), F::add(V, V)); // S
        Elem Y3 = F::sub(F::mul(R, F::sub(V, X3)), F::mul(S1, HHH)); // 2M
        Elem Z3 = F::mul(F::mul(a.Z, b.Z), H);   // 2M
        return from_affine_xz(X3, Y3, Z3);
    }
    // mixed add (b affine, i.e. Z2 = 1): 8M+3S
    static Jacobian add_affine(const Jacobian& a, const Affine<F>& b) {
        if (a.is_zero()) { Jacobian j = from_affine(b.x, b.y); return j; }
        if (b.is_zero()) return a;
        Elem Z1Z1 = F::sqr(a.Z);            // S
        Elem U2 = F::mul(b.x, Z1Z1);        // M
        Elem S2 = F::mul(b.y, F::mul(Z1Z1, a.Z)); // 2M
        if (U2 == a.X) {
            if (S2 == a.Y) return dbl(a);
            return zero();
        }
        Elem H = F::sub(U2, a.X);
        Elem R = F::sub(S2, a.Y);
        Elem HH = F::sqr(H);                // S
        Elem HHH = F::mul(H, HH);           // M
        Elem V = F::mul(a.X, HH);           // M
        Elem X3 = F::sub(F::sub(F::sqr(R), HHH), F::add(V, V)); // S
        Elem Y3 = F::sub(F::mul(R, F::sub(V, X3)), F::mul(a.Y, HHH)); // 2M
        Elem Z3 = F::mul(a.Z, H);           // M
        return from_affine_xz(X3, Y3, Z3);
    }

    // scalar mult (general Jacobian double-and-add; correct for any base)
    static Jacobian mul(const Jacobian& p, uint64_t k) {
        Jacobian r = zero();
        Jacobian b = p;
        while (k) {
            if (k & 1) r = add(r, b);
            b = dbl(b);
            k >>= 1;
        }
        return r;
    }

    Affine<F> to_affine() const {
        if (is_zero()) return Affine<F>::zero();
        Elem zi = F::inv(Z);
        Elem zi2 = F::sqr(zi);
        return Affine<F>::rep(F::mul(X, zi2), F::mul(Y, F::mul(zi2, zi)));
    }
};

} // namespace ec