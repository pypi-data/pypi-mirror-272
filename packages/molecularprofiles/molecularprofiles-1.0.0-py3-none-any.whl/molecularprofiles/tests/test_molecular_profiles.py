import os
import pytest
import numpy as np
from astropy.table import Table
from astropy.units import Quantity
from molecularprofiles.molecularprofiles import MolecularProfile

# Define the path to the test data directory
TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")


@pytest.fixture
def empty_mol_profile():
    # Define the path to the test grib file
    grib_file_path = os.path.join(TEST_DATA_DIR, "grib/sample.grib")
    # Create and return the MolecularProfile instance
    return MolecularProfile(grib_file_path)


@pytest.fixture
def mol_profile(empty_mol_profile):
    empty_mol_profile.get_data()
    return empty_mol_profile


def test_get_data(empty_mol_profile):
    # Test get_data method
    empty_mol_profile.get_data()
    # Perform assertions
    assert empty_mol_profile.data is not None
    assert empty_mol_profile.stat_data is not None
    assert empty_mol_profile.stat_description is not None
    assert isinstance(empty_mol_profile.data, Table)
    with pytest.raises(FileNotFoundError):
        t_mol_profile = MolecularProfile("/foo/bar/baz.grib")
        t_mol_profile.get_data()


def test_write_atmospheric_profile(mol_profile):
    # Define test parameters
    outfile = "test_atmospheric_profile.ecsv"
    outfile_bad = "test_atmospheric_profile.txt"
    co2_concentration = 415  # Placeholder value
    reference_atmosphere = None  # Placeholder value
    # Test write_atmospheric_profile method
    with pytest.raises(SystemExit):
        mol_profile.write_atmospheric_profile(
            outfile_bad, co2_concentration, reference_atmosphere
        )
    mol_profile.write_atmospheric_profile(
        outfile, co2_concentration, reference_atmosphere
    )
    # Perform assertions
    assert os.path.isfile(outfile)


def test_create_mdp(mol_profile):
    # Define test parameters
    mdp_file = "test_mdp_file.ecsv"
    # Test create_mdp method
    mol_profile.create_mdp(mdp_file)
    # Perform assertions
    assert os.path.isfile(mdp_file)


def test_rayleigh_extinction(mol_profile):
    # Define test parameters
    rayleigh_extinction_file = "test_rayleigh_extinction_file.ecsv"
    co2_concentration = 415  # Placeholder value
    wavelength_min = Quantity(340, unit="nm")  # Placeholder value
    wavelength_max = Quantity(360, unit="nm")  # Placeholder value
    # Test rayleigh_extinction method
    mol_profile.rayleigh_extinction(
        rayleigh_extinction_file,
        co2_concentration,
        wavelength_min,
        wavelength_max,
    )
    # Perform assertions
    assert os.path.isfile(rayleigh_extinction_file)


def test_convert_to_simtel_compatible(mol_profile):
    # Define test parameters
    input_ecsv_file = os.path.join(
        TEST_DATA_DIR, "ecsv/test_rayleigh_extinction_file.ecsv"
    )
    output_file = "test_rayleigh_extinction_profile_simtel.txt"
    observation_altitude = Quantity(5000, unit="m")
    # Test convert_to_simtel_compatible method
    mol_profile.convert_to_simtel_compatible(
        input_ecsv_file, output_file, observation_altitude
    )
    # Perform assertions
    assert os.path.isfile(output_file)


def test_timeseries_analysis(mol_profile):
    # Define test parameters
    outfile = "test_timeseries_analysis.ecsv"
    t_floor = Quantity(100, unit="m")
    t_ceiling = Quantity(2000, unit="m")
    # Test timeseries_analysis method
    mol_profile.timeseries_analysis(outfile, m_floor=t_floor, m_ceiling=t_ceiling)
    # Perform assertions
    assert os.path.isfile(outfile)
