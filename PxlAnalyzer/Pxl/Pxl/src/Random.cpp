// Random.cpp is based on Random.h
// Mersenne Twister random number generator -- a C++ class Random
// Based on code by Makoto Matsumoto, Takuji Nishimura, and Shawn Cokus
// Richard J. Wagner  v1.0  15 May 2003  rjwagner@writeme.com

// The Mersenne Twister is an algorithm for generating random numbers.  It
// was designed with consideration of the flaws in various other generators.
// The period, 2^19937-1, and the order of equidistribution, 623 dimensions,
// are far greater.  The generator is also fast; it avoids multiplication and
// division, and it benefits from caches and pipelines.  For more information
// see the inventors' web page at http://www.math.keio.ac.jp/~matumoto/emt.html

// Reference
// M. Matsumoto and T. Nishimura, "Mersenne Twister: A 623-Dimensionally
// Equidistributed Uniform Pseudo-Random Number Generator", ACM Transactions on
// Modeling and Computer Simulation, Vol. 8, No. 1, January 1998, pp 3-30.

// Copyright (C) 1997 - 2002, Makoto Matsumoto and Takuji Nishimura,
// Copyright (C) 2000 - 2003, Richard J. Wagner
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions
// are met:
//
//   1. Redistributions of source code must retain the above copyright
//      notice, this list of conditions and the following disclaimer.
//
//   2. Redistributions in binary form must reproduce the above copyright
//      notice, this list of conditions and the following disclaimer in the
//      documentation and/or other materials provided with the distribution.
//
//   3. The names of its contributors may not be used to endorse or promote
//      products derived from this software without specific prior written
//      permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
// CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
// EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
// PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
// PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
// LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
// NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
// SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

// The original code included the following notice:
//
//     When you use this, send an email to: matumoto@math.keio.ac.jp
//     with an appropriate reference to your work.
//
// It would be nice to CC: rjwagner@writeme.com and Cokus@math.washington.edu
// when you write.

// Parts of this file are modified beginning in 29.10.09 for adaption in
// PXL.

#include "Pxl/Pxl/interface/pxl/core/Random.hpp"
#include "Pxl/Pxl/interface/pxl/core/RotationMatrix.hpp"

namespace pxl
{

Random::Random(const uint32 &oneSeed)
{
    seed(oneSeed);
}

Random::Random(uint32 *const bigSeed, const uint32 seedLength)
{
    seed(bigSeed, seedLength);
}

Random::Random()
{
    seed();
}

double Random::rand()
{
    return double(randInt()) * (1.0 / 4294967295.0);
}

double Random::rand(const double &n)
{
    return rand() * n;
}

double Random::randExc()
{
    return double(randInt()) * (1.0 / 4294967296.0);
}

double Random::randExc(const double &n)
{
    return randExc() * n;
}

double Random::randDblExc()
{
    return (double(randInt()) + 0.5) * (1.0 / 4294967296.0);
}

double Random::randDblExc(const double &n)
{
    return randDblExc() * n;
}

double Random::rand53()
{
    uint32 a = randInt() >> 5, b = randInt() >> 6;
    return (a * 67108864.0 + b) * (1.0 / 9007199254740992.0); // by Isaku Wada
}

double Random::randNorm(const double &mean, const double &variance)
{
    // Return a real number from a normal (Gaussian) distribution with given
    // mean and variance by Box-Muller method
    double r = sqrt(-2.0 * log(1.0 - randDblExc())) * variance;
    double phi = 2.0 * 3.14159265358979323846264338328 * randExc();
    return mean + r * cos(phi);
}

double Random::randUniform(double min, double max)
{
    return min + (max - min) * this->rand();
}

/// returns a rayleigh distributed value
double Random::randRayleigh(double sigma)
{
    return sigma * sqrt(-2.0 * log(1 - this->rand()));
}

double Random::randFisher(double k)
{
    return acos(1. + 1. / k * log(1 - rand() * (1 - exp(-2 * k))));
}

Basic3Vector Random::randFisher(const Basic3Vector &meanDirection, double kappa)
{
    double alpha = randFisher(kappa);

    Basic3Vector rotDirection = randUnitVectorOnSphere();
    Basic3Vector rotAxis = meanDirection.cross(rotDirection);
    rotAxis.normalize();

    RotationMatrix M(rotAxis, alpha);
    Basic3Vector vnew = M * meanDirection;

    return vnew;
}

Basic3Vector Random::randFisher(const Basic3Vector *meanDirection, double kappa)
{
    return randFisher(*meanDirection, kappa);
}

Basic3Vector Random::randUnitVectorOnSphere()
{
    double z = this->randUniform(-1.0, 1.0);
    double t = this->randUniform(-1.0 * M_PI, M_PI);
    double r = sqrt(1 - z * z);
    return Basic3Vector(r * cos(t), r * sin(t), z);
}

double Random::randPowerLaw(double index, double min, double max)
{
    if ((min <= 0) || (max < min))
    {
        throw std::runtime_error("Power law distribution only possible for 0 < min <= max");
    }
    // index = -1
    if ((std::abs(index + 1.0)) < DBL_EPSILON)
    {
        double part1 = log(max);
        double part2 = log(min);
        return exp((part1 - part2) * this->rand() + part2);
    }
    else
    {
        double part1 = pow(max, index + 1);
        double part2 = pow(min, index + 1);
        double ex = 1 / (index + 1);
        return pow((part1 - part2) * this->rand() + part2, ex);
    }
}

double Random::randBrokenPowerLaw(double index1, double index2, double breakpoint, double min, double max)
{
    if ((min <= 0) || (max < min))
    {
        throw std::runtime_error("Power law distribution only possible for 0 < min <= max");
    }
    if (min >= breakpoint)
    {
        return this->randPowerLaw(index2, min, max);
    }
    else if (max <= breakpoint)
    {
        return this->randPowerLaw(index2, min, max);
    }
    else
    {
        double intPL1;
        // check if index1 = -1
        if ((std::abs(index1 + 1.0)) < DBL_EPSILON)
        {
            intPL1 = log(breakpoint / min);
        }
        else
        {
            intPL1 = (pow(breakpoint, index1 + 1) - pow(min, index1 + 1)) / (index1 + 1);
        }
        double intPL2;
        // check if index2 = -1
        if ((std::abs(index2 + 1.0)) < DBL_EPSILON)
        {
            intPL2 = log(max / breakpoint) * pow(breakpoint, index1 - index2);
        }
        else
        {
            intPL2 =
                (pow(max, index2 + 1) - pow(breakpoint, index2 + 1)) * pow(breakpoint, index1 - index2) / (index2 + 1);
        }
        if (this->rand() > intPL1 / (intPL1 + intPL2))
            return this->randPowerLaw(index2, breakpoint, max);
        else
            return this->randPowerLaw(index1, min, breakpoint);
    }
}

double Random::randExponential()
{
    double dum;
    do
    {
        dum = this->rand();
    } while (dum < DBL_EPSILON);
    return -1.0 * log(dum);
}

Random::uint32 Random::randInt()
{

    if (left == 0)
        reload();
    --left;

    uint32 s1;
    s1 = *pNext++;
    s1 ^= (s1 >> 11);
    s1 ^= (s1 << 7) & 0x9d2c5680UL;
    s1 ^= (s1 << 15) & 0xefc60000UL;
    return (s1 ^ (s1 >> 18));
}

Random::uint32 Random::randInt(const uint32 &n)
{
    // Find which bits are used in n
    // Optimized by Magnus Jonsson (magnus@smartelectronix.com)
    uint32 used = n;
    used |= used >> 1;
    used |= used >> 2;
    used |= used >> 4;
    used |= used >> 8;
    used |= used >> 16;

    // Draw numbers until one is found in [0,n]
    uint32 i;
    do
        i = randInt() & used; // toss unused bits to shorten search
    while (i > n);
    return i;
}

void Random::seed(const uint32 oneSeed)
{
    initialize(oneSeed);
    reload();
}

void Random::seed(uint32 *const bigSeed, const uint32 seedLength)
{
    initialize(19650218UL);
    int i = 1;
    uint32 j = 0;
    int k = (N > seedLength ? N : seedLength);
    for (; k; --k)
    {
        state[i] = state[i] ^ ((state[i - 1] ^ (state[i - 1] >> 30)) * 1664525UL);
        state[i] += (bigSeed[j] & 0xffffffffUL) + j;
        state[i] &= 0xffffffffUL;
        ++i;
        ++j;
        if (i >= N)
        {
            state[0] = state[N - 1];
            i = 1;
        }
        if (j >= seedLength)
            j = 0;
    }
    for (k = N - 1; k; --k)
    {
        state[i] = state[i] ^ ((state[i - 1] ^ (state[i - 1] >> 30)) * 1566083941UL);
        state[i] -= i;
        state[i] &= 0xffffffffUL;
        ++i;
        if (i >= N)
        {
            state[0] = state[N - 1];
            i = 1;
        }
    }
    state[0] = 0x80000000UL; // MSB is 1, assuring non-zero initial array
    reload();
}

void Random::seed()
{

    // First try getting an array from /dev/urandom
    FILE *urandom = fopen("/dev/urandom", "rb");
    if (urandom)
    {
        uint32 bigSeed[N];
        uint32 *s = bigSeed;
        int i = N;
        bool success = true;
        while (success && i--)
            success = fread(s++, sizeof(uint32), 1, urandom) != 0;
        fclose(urandom);
        if (success)
        {
            seed(bigSeed, N);
            return;
        }
    }

    // Was not successful, so use time() and clock() instead
    seed(hash(time(NULL), clock()));
}

void Random::initialize(const uint32 seed)
{
    uint32 *s = state;
    uint32 *r = state;
    int i = 1;
    *s++ = seed & 0xffffffffUL;
    for (; i < N; ++i)
    {
        *s++ = (1812433253UL * (*r ^ (*r >> 30)) + i) & 0xffffffffUL;
        r++;
    }
}

void Random::reload()
{
    uint32 *p = state;
    int i;
    for (i = N - M; i--; ++p)
        *p = twist(p[M], p[0], p[1]);
    for (i = M; --i; ++p)
        *p = twist(p[M - N], p[0], p[1]);
    *p = twist(p[M - N], p[0], state[0]);

    left = N, pNext = state;
}

Random::uint32 Random::hash(time_t t, clock_t c)
{

    static uint32 differ = 0; // guarantee time-based seeds will change

    uint32 h1 = 0;
    unsigned char *p = (unsigned char *)&t;
    for (size_t i = 0; i < sizeof(t); ++i)
    {
        h1 *= UCHAR_MAX + 2U;
        h1 += p[i];
    }
    uint32 h2 = 0;
    p = (unsigned char *)&c;
    for (size_t j = 0; j < sizeof(c); ++j)
    {
        h2 *= UCHAR_MAX + 2U;
        h2 += p[j];
    }
    return (h1 + differ++) ^ h2;
}

void Random::save(uint32 *saveArray) const
{
    uint32 *sa = saveArray;
    const uint32 *s = state;
    int i = N;
    for (; i--; *sa++ = *s++)
    {
    }
    *sa = left;
}

void Random::load(uint32 *const loadArray)
{
    uint32 *s = state;
    uint32 *la = loadArray;
    int i = N;
    for (; i--; *s++ = *la++)
    {
    }
    left = *la;
    pNext = &state[N - left];
}

std::ostream &operator<<(std::ostream &os, const Random &mtrand)
{
    const Random::uint32 *s = mtrand.state;
    int i = mtrand.N;
    for (; i--; os << *s++ << "\t")
    {
    }
    return os << mtrand.left;
}

std::istream &operator>>(std::istream &is, Random &mtrand)
{
    Random::uint32 *s = mtrand.state;
    int i = mtrand.N;
    for (; i--; is >> *s++)
    {
    }
    is >> mtrand.left;
    mtrand.pNext = &mtrand.state[mtrand.N - mtrand.left];
    return is;
}

} // namespace pxl
