import sys, struct, os

def main():

	#Reading the commandline arguments
	if len(sys.argv) != 3:
		print "USAGE: %s <BOOTLOADER_IMAGE> <OUTPUT_DIR>" % sys.argv[0]
		return
	bootloader_path = sys.argv[1]
	output_path = sys.argv[2]

	#Verifying the magic
	bootloader_file = open(bootloader_path, 'rb')
	magic = bootloader_file.read(8)
	if magic != "BOOTLDR!":
		print "[-] Read incorrect magic: %s" % magic.encode("hex")
		return
	print "[+] Read correct magic"

	#Reading in the metadata block
	image_count,data_start_addr,total_size = struct.unpack("<III", bootloader_file.read(12))
	print "[+] Found %d images, starting at %08X, total size: %08X" % (image_count, data_start_addr, total_size)
	image_metadata = []
	for i in range(0, image_count):
		image_name = bootloader_file.read(64).strip('\x00')
		image_len = struct.unpack("<I", bootloader_file.read(4))[0]
		image_metadata.append((image_name, image_len))
	print "[+] Images: %s" % str(image_metadata)

	#Dumping each image
	bootloader_file.seek(data_start_addr, 0)
	for image_name, image_len in image_metadata:
		print "[+] Dumping %s" % image_name
		data = bootloader_file.read(image_len)
		open(os.path.join(output_path, image_name), 'wb').write(data)
	print "[+] Done"

if __name__ == "__main__":
	main()
