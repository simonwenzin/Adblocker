from engine.evaluate import evaluate

def main():
    domain = input("Enter DOMAIN: ")
    decision = evaluate(domain)
    print(decision)


if __name__ == "__main__":
    main()
