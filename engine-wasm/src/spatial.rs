//! Spatial calculations and bounding box filtering for MythosAtlas.

use std::f32::consts::PI;

/// Earth radius in kilometers (approximate spherical model)
pub const EARTH_RADIUS_KM: f32 = 6371.0;

#[derive(Clone, Copy, Debug)]
pub struct GeoCoord {
    pub lat: f32,
    pub lng: f32,
}

impl GeoCoord {
    pub fn new(lat: f32, lng: f32) -> Self {
        Self { lat, lng }
    }

    /// Converts latitude and longitude in degrees to a 3D unit vector on the globe.
    /// Uses standard Three.js spherical coordinate conventions:
    /// Y is Up, Z is toward prime meridian (0° lon), X is toward 90° E.
    pub fn to_cartesian_unit(&self, radius: f32) -> [f32; 3] {
        let phi = (90.0 - self.lat) * (PI / 180.0);
        let theta = (self.lng + 180.0) * (PI / 180.0);

        let x = -(radius * phi.sin() * theta.cos());
        let y = radius * phi.cos();
        let z = radius * phi.sin() * theta.sin();

        [x, y, z]
    }

    /// Calculates Great Circle Distance between two coordinates in kilometers using Haversine formula.
    pub fn distance_to(&self, other: &GeoCoord) -> f32 {
        let lat1_rad = self.lat * (PI / 180.0);
        let lat2_rad = other.lat * (PI / 180.0);
        let delta_lat = (other.lat - self.lat) * (PI / 180.0);
        let delta_lng = (other.lng - self.lng) * (PI / 180.0);

        let a = (delta_lat / 2.0).sin().powi(2)
            + lat1_rad.cos() * lat2_rad.cos() * (delta_lng / 2.0).sin().powi(2);
        let c = 2.0 * a.sqrt().atan2((1.0 - a).sqrt());

        EARTH_RADIUS_KM * c
    }

    /// Checks if coordinate is contained inside a bounding box.
    pub fn within_bounds(&self, min_lat: f32, max_lat: f32, min_lng: f32, max_lng: f32) -> bool {
        self.lat >= min_lat && self.lat <= max_lat && self.lng >= min_lng && self.lng <= max_lng
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cartesian_unit() {
        // North Pole (90, 0)
        let np = GeoCoord::new(90.0, 0.0);
        let [x, y, z] = np.to_cartesian_unit(1.0);
        assert!((y - 1.0).abs() < 1e-4);
        assert!(x.abs() < 1e-4);
        assert!(z.abs() < 1e-4);
    }

    #[test]
    fn test_great_circle_distance() {
        // Babylon (32.53, 44.42) to Uruk (31.32, 45.63)
        let babylon = GeoCoord::new(32.53, 44.42);
        let uruk = GeoCoord::new(31.32, 45.63);
        let dist = babylon.distance_to(&uruk);
        // Approximately 180-200 km
        assert!(dist > 150.0 && dist < 220.0, "Expected dist ~180km, got {}", dist);
    }
}
