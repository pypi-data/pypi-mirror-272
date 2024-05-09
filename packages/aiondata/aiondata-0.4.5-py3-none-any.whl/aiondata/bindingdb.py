import io
from typing import Optional, Generator, Union, Tuple
import urllib.request
from rdkit import Chem
from rdkit import RDLogger
from tqdm.auto import tqdm
import zipfile

from .datasets import GeneratedDataset


class BindingDB(GeneratedDataset):
    """BindingDB

    A public, web-accessible database of measured binding affinities, focusing chiefly on the interactions of protein considered to be drug-targets with small, drug-like molecules.
    """

    SOURCE = "https://www.bindingdb.org/bind/downloads/BindingDB_All_3D_202402_sdf.zip"
    COLLECTION = "bindingdb"

    float_fields = {
        "Ki (nM)",
        "IC50 (nM)",
        "Kd (nM)",
        "EC50 (nM)",
        "kon (M-1-s-1)",
        "koff (s-1)",
    }

    def __init__(self, fd: Optional[io.BufferedReader] = None):
        """
        Initializes a BindingDB instance.

        Args:
            fd (Optional[io.BufferedReader]): The file-like object containing the dataset content.
                If `fd` is not provided, the dataset content will be fetched from the default source.
        """
        if fd is None:
            cached_sdf = self.get_cache_path().parent / "BindingDB.sdf.zip"
            if cached_sdf.exists():
                self.outer_fd, self.fd = self.from_compressed_file(cached_sdf)
            else:
                self.outer_fd, self.fd = self.from_url(self.SOURCE)
        else:
            self.outer_fd, self.fd = fd

    def _convert_to_numeric(
        self, prop_name: str, value: str
    ) -> Union[int, float, str, None]:
        """
        Converts a property value to numeric type.

        Args:
            prop_name (str): The name of the property.
            value (str): The value of the property.

        Returns:
            The converted numeric value, or None if conversion fails.
        """
        if prop_name in BindingDB.float_fields:
            try:
                return float(value)
            except ValueError:
                return None
        else:
            try:
                float_value = float(value)
                if float_value.is_integer():
                    return int(float_value)
                else:
                    return float_value
            except ValueError:
                return value

    @staticmethod
    def from_url(url: str) -> Tuple[zipfile.ZipFile, io.BufferedReader]:
        """
        Creates a BindingDB instance from a URL containing a compressed SDF file, using streaming.

        Args:
            url (str): The URL of the dataset.

        Returns:
            A tuple containing the ZipFile instance and a BufferedReader instance containing the content of the SDF file.
        """
        response = urllib.request.urlopen(url)
        return BindingDB.from_compressed_file(io.BytesIO(response.read()))

    @staticmethod
    def from_compressed_file(
        file_path: str,
    ) -> Tuple[zipfile.ZipFile, io.BufferedReader]:
        """
        Creates a BindingDB instance from a compressed SDF file.

        Args:
            file_path (str): The path to the compressed file.

        Returns:
            A tuple containing the ZipFile instance and a BufferedReader instance containing the content of the SDF file.
        """
        zip_file = zipfile.ZipFile(file_path)
        sdf_name = zip_file.namelist()[0]
        sdf_file = zip_file.open(sdf_name)
        sdf_content = io.BufferedReader(sdf_file)
        return zip_file, sdf_content

    @staticmethod
    def from_uncompressed_file(file_path: str) -> io.BufferedReader:
        """
        Creates a BindingDB instance from an uncompressed SDF file.

        Args:
            file_path (str): The path to the uncompressed file.

        Returns:
            A BufferedReader instance containing the content of the SDF file.
        """
        return None, open(file_path, "rb")

    def to_generator(self, progress_bar: bool = True) -> Generator[dict, None, None]:
        """
        Converts the dataset to a generator.

        Args:
            progress_bar (bool): Whether to display a progress bar.

        Yields:
            dict: A dictionary representing a record in the dataset.
        """
        RDLogger.DisableLog("rdApp.*")  # Suppress RDKit warnings and errors

        if progress_bar:
            pb = tqdm
        else:

            def pb(x, **kwargs):
                return x

        with Chem.ForwardSDMolSupplier(self.fd, sanitize=True, removeHs=False) as sd:
            for mol in pb(sd, desc="Parsing BindingDB", unit=" molecules"):
                if mol is not None:
                    record = {
                        prop: self._convert_to_numeric(prop, mol.GetProp(prop))
                        for prop in mol.GetPropNames()
                        if mol.HasProp(prop)
                    }

                    # Normalize PubChem SID and CID fields that are sometimes present in the SDF
                    if "PubChem SID" in record:
                        record["PubChem SID of Ligand"] = record.pop("PubChem SID")
                    if "PubChem CID" in record:
                        record["PubChem CID of Ligand"] = record.pop("PubChem CID")

                    record["SMILES"] = Chem.MolToSmiles(mol)
                    yield record

        self.fd.close()
        if self.outer_fd is not None:
            self.outer_fd.close()

        # Re-enable logging
        RDLogger.EnableLog("rdApp.error")
        RDLogger.EnableLog("rdApp.warning")
