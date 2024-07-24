import unittest

from kyber_py.kyber import Kyber512, Kyber768, Kyber1024
from kyber_py.ml_kem import ML_KEM_512, ML_KEM_768, ML_KEM_1024

algs = {
    "Kyber-512": Kyber512,
    "Kyber-768": Kyber768,
    "Kyber-1024": Kyber1024,
    "ML-KEM-512": ML_KEM_512,
    "ML-KEM-768": ML_KEM_768,
    "ML-KEM-1024": ML_KEM_1024,
}

class TestGSVPublicKeyCompression(unittest.TestCase):

    def generic_gsvcompression_test(self, alg_name):
        Alg = algs[alg_name]
        pk, sk = Alg.keygen()

        t_hat_bytes, rho = pk[:-32], pk[-32:]
        t_hat = Alg.M.decode_vector(t_hat_bytes, Alg.k, 12, is_ntt=True)
        encoded = t_hat.gsvcompression_encode()
        decoded = Alg.M.gsvcompression_decode_vector(encoded, Alg.k, is_ntt=True)
        self.assertEqual(t_hat, decoded)

        print(alg_name)
        print(f"original public key size: {len(t_hat_bytes) + 32}")
        print(f"gsv_encoded public key size: {len(encoded) + 32}")

    def test_kyber512(self):
        self.generic_gsvcompression_test("Kyber-512")
    def test_kyber768(self):
        self.generic_gsvcompression_test("Kyber-768")
    def test_kyber1024(self):
        self.generic_gsvcompression_test("Kyber-1024")
    def test_mlkem512(self):
        self.generic_gsvcompression_test("ML-KEM-512")
    def test_mlkem768(self):
        self.generic_gsvcompression_test("ML-KEM-768")
    def test_mlkem1024(self):
        self.generic_gsvcompression_test("ML-KEM-1024")
