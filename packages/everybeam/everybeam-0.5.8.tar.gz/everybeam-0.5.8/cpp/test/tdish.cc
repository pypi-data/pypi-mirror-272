// Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
// SPDX-License-Identifier: GPL-3.0-or-later

#include <boost/test/unit_test.hpp>

#include "config.h"
#include "../load.h"
#include "../options.h"
#include "../pointresponse/dishpoint.h"
#include "../telescope/dish.h"
#include "../coords/itrfconverter.h"

namespace everybeam {
namespace {
// First time stamp in mock ms"
const double kTime = 5068498314.005126;
const double kFrequency = 8.56313e+08;
const double kRa = 0.90848969;
const double kDec = -0.48149271;

}  // namespace

BOOST_AUTO_TEST_SUITE(dish)

BOOST_AUTO_TEST_CASE(load_dish) {
  everybeam::Options options;

  casacore::MeasurementSet ms(DISH_MOCK_PATH);

  std::unique_ptr<everybeam::telescope::Telescope> telescope =
      everybeam::Load(ms, options);

  // Check that we have an Dish pointer.
  const everybeam::telescope::Dish* dish_telescope =
      dynamic_cast<const everybeam::telescope::Dish*>(telescope.get());
  BOOST_REQUIRE(dish_telescope);

  // Assert if correct number of stations
  BOOST_CHECK_EQUAL(dish_telescope->GetNrStations(), size_t{62});

  // Assert that we have a dish point response
  std::unique_ptr<everybeam::pointresponse::PointResponse> point_response =
      dish_telescope->GetPointResponse(kTime);
  everybeam::pointresponse::DishPoint* dish_point_response =
      dynamic_cast<everybeam::pointresponse::DishPoint*>(point_response.get());
  BOOST_REQUIRE(dish_point_response);

  const std::vector<std::vector<std::complex<float>>> kReferenceResponse = {
      {{1.0, 0.0}, {0.0, 0.0}, {0.0, 0.0}, {1.0, 0.0}},
      {{0.382599, 0.0}, {0.0, 0.0}, {0.0, 0.0}, {0.382599, 0.0}}};

  std::vector<std::pair<double, double>> offsets = {{0.0, 0.0}, {0.01, -0.02}};

  for (size_t j = 0; j < offsets.size(); j++) {
    // Check the two response functions
    double ra = kRa + offsets[j].first;
    double dec = kDec + offsets[j].second;
    size_t station_id = 0;
    size_t field_id = 0;

    std::array<std::complex<float>, 4> point_response_buffer;
    dish_point_response->Response(everybeam::BeamMode::kFull,
                                  point_response_buffer.data(), ra, dec,
                                  kFrequency, station_id, field_id);

    for (std::size_t i = 0; i < 4; ++i) {
      BOOST_CHECK_CLOSE(point_response_buffer[i], kReferenceResponse[j][i],
                        2.0e-4);
    }

    casacore::MDirection pointing(casacore::Quantity(ra, "rad"),
                                  casacore::Quantity(dec, "rad"),
                                  casacore::MDirection::J2000);

    const coords::ItrfConverter itrf_converter(kTime);
    vector3r_t direction = itrf_converter.ToItrf(pointing);

    const aocommon::MC2x2 response = dish_point_response->Response(
        everybeam::BeamMode::kFull, station_id, kFrequency, direction);

    for (std::size_t i = 0; i < 4; ++i) {
      BOOST_CHECK_CLOSE(response[i],
                        std::complex<double>(kReferenceResponse[j][i]), 2.0e-4);
    }
  }
}

BOOST_AUTO_TEST_SUITE_END()

}  // namespace everybeam
