import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-n', 
        '--num',
        help="This is the number",
        required=True
    )
    
    args = vars(parser.parse_args())

    print(parser.parse_args())

    number = args.get("num")

    print(number)
