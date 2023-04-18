def main():
    count = 0
    with open('4_digits_pin_list.txt', 'a') as f:
        while count < 10000:
            f.write(str(count).zfill(4)+"\n")
            count += 1
    f.close()


main()
