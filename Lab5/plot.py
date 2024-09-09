import matplotlib.pyplot as plt

X = [0.1158656, 0.0579328, 0.0289664, 0.0193109, 0.0144832]
Y_practical_Purealoha = [0.046687200, 0.024767440, 0.016838652, 0.012728280, 0.0102106]
Y_theoretical_Purealoha = [0.047183604, 0.024860887, 0.016865925, 0.012760402, 0.01026185]

Y_practical_slottedaloha = [0.049581600, 0.024790800, 0.016527186, 0.012395400, 0.009916320]
Y_theoretical_slottedaloha = [0.049721773, 0.025520805, 0.017163083, 0.012928652, 0.010369960]

plt.figure(figsize=(10, 6))
plt.plot(X, Y_practical_slottedaloha, 'o-', color='blue', label='Practical', markersize=8)
plt.plot(X, Y_theoretical_slottedaloha, '-', color='red', label='Theoretical')
plt.plot(X, Y_practical_Purealoha, "^", color='green', label='Purealoha', markersize=8)
plt.plot(X, Y_theoretical_Purealoha, '-', color='yellow', label='Theoretical')

plt.xlabel('G values')
plt.ylabel('S values')
plt.title('Practical vs Theoretical Comparison')
plt.legend()
plt.grid(True)

plt.show()
