# For MD5 (128 bits)
md5_int1 = int('a69a785968cd110f4880e16aa2760087', 16)
md5_int2 = int('84d6475271f291fc25a3d253636a32e3', 16)
xor_md5 = md5_int1 ^ md5_int2
diff_bits_md5 = bin(xor_md5).count('1')
same_bits_md5 = 128 - diff_bits_md5
print('MD5 same bits:', same_bits_md5)  # Output: 70

# For SHA256 (256 bits)
sha256_int1 = int('a1668d6acc3a96ea04fb63621402daed006193348323c9718d816cce1359423c', 16)
sha256_int2 = int('e8b6f8216799253e8eb6a0edf21b53017a4f01a64986f0f67bc54088b93bea7c', 16)
xor_sha256 = sha256_int1 ^ sha256_int2
diff_bits_sha256 = bin(xor_sha256).count('1')
same_bits_sha256 = 256 - diff_bits_sha256
print('SHA256 same bits:', same_bits_sha256)  # Output: 135