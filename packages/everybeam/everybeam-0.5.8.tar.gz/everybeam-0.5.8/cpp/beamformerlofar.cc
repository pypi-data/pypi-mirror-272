// Copyright (C) 2022 ASTRON (Netherlands Institute for Radio Astronomy)
// SPDX-License-Identifier: GPL-3.0-or-later

#include "beamformerlofar.h"
#include "beamformer.h"

#include "common/constants.h"
#include "common/mathutils.h"

#include <cmath>
#include <cassert>

namespace everybeam {
aocommon::MC2x2Diag BeamFormerLofar::FieldArrayFactor(
    [[maybe_unused]] real_t time, real_t freq, const vector3r_t& direction,
    const Options& options, const std::vector<vector3r_t>& antenna_positions,
    const std::vector<std::array<bool, 2>>& antenna_enabled) const {
  assert(antenna_positions.size() == antenna_enabled.size());

  // Weighted subtraction of the directions, with weights given by corresponding
  // freqs. Purpose is to correctly handle the case in which options.freq0 !=
  // freq
  const vector3r_t delta_direction =
      options.freq0 * options.station0 - freq * direction;

  // Get geometric response for pointing direction
  aocommon::UVector<std::complex<double>> geometric_response =
      BeamFormer::ComputeGeometricResponse(antenna_positions, delta_direction);

  std::array<std::complex<double>, 2> response_sum = {0.0, 0.0};
  std::array<double, 2> weight_sum = {0.0, 0.0};

  for (size_t idx = 0; idx < antenna_positions.size(); ++idx) {
    response_sum[0] +=
        geometric_response[idx] * (1.0 * antenna_enabled[idx][0]);
    response_sum[1] +=
        geometric_response[idx] * (1.0 * antenna_enabled[idx][1]);
    weight_sum[0] += (1.0 * antenna_enabled[idx][0]);
    weight_sum[1] += (1.0 * antenna_enabled[idx][1]);
  }

  // Normalize the weight by the number of enabled tiles
  return aocommon::MC2x2Diag(response_sum[0] / weight_sum[0],
                             response_sum[1] / weight_sum[1]);
}

aocommon::MC2x2 BeamFormerLofar::LocalResponse(
    const ElementResponse& element_response, real_t time, real_t freq,
    const vector3r_t& direction, const Options& options) const {
  // Compute the combined array factor
  const aocommon::MC2x2Diag array_factor =
      LocalArrayFactor(time, freq, direction, options);

  // NOTE: there are maybe some redundant transformations in element-> response
  const aocommon::MC2x2 response =
      element_->Response(element_response, time, freq, direction, options);
  return array_factor * response;
}

}  // namespace everybeam
