import os
import hashlib

def _generate_hashes(info):
    hash_file_path = os.path.join(info.output, "sha256hashes.csv")
    successful = 0
    
    try:
        hash_file = open(hash_file_path, 'w+')

        for root, dirs, files in os.walk(info.input):
            for name in files:
                file_path = os.path.join(root, name)

                with open(file_path, 'rb') as file_to_hash:
                    file_hash = hashlib.sha256()

                    # We need to do this to ensure we don't fail for large input sizes
                    for b_block in iter(lambda: file_to_hash.read(4096),b""):
                        file_hash.update(b_block)

                hash_file.write(f"\"{os.path.relpath(file_path, info.input)}\",{file_hash.hexdigest()}\n")
                successful += 1

    except Exception as e:
        info.log.error(f"Encounted an error when hashing files: {e}")

        return False
    finally:
        hash_file.close()

    info.log.info(f"Generated a total of '{successful}' sha256 file hashes")

    return True

def run(info):
    return _generate_hashes(info)