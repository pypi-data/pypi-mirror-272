# EveryBeam Changelog

## 0.5.8

- Fix AVX-enabled EveryBeam

### Improvements

- Implement caching for NCP direction, which speeds up computation of e.g. DP3 Predict.

## 0.5.7
- Implement Response function for dish telescopes, to enable usage in DP3.

### Improvements
- EveryBeam no longer indirectly depends on the GSL library, via schaapcommon.
