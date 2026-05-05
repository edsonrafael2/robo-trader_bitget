from strategies.risk_management import RiskManagement

entry_price = 100
rm = RiskManagement(entry_price)

prices = [100.2,100.6,100.9,101.1,101.3,100.8,100.4]

for price in prices:

    result = rm.update(price)

    print(f"Preço: {price} | Estado: {result}")

    if result in ["STOP", "TAKE_PROFIT"]:
        print("Operação encerrada")
        break


# from strategies.risk_management import RiskManagement

# entry_price = 100

# rm = RiskManagement(entry_price)

# prices = [100.2,100.6,100.9,101.1,101.3,100.8,100.4]

# for price in prices:

#     result = rm.update(price)

#     print(f"Preço: {price} | Estado: {result}")