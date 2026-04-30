import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("output/results.csv")

# pisahin data berdasarkan status
df_new = df[df["Status"] == "NEW_PATH"]
df_cache = df[df["Status"] == "CACHE_HIT"]
df_replan = df[df["Status"] == "REPLAN"]

plt.figure(figsize=(8, 5))

# scatter per kategori
plt.scatter(df_new["Step"], df_new["Time"], color="blue", label="NEW_PATH")
plt.scatter(df_cache["Step"], df_cache["Time"], color="green", label="CACHE_HIT")
plt.scatter(df_replan["Step"], df_replan["Time"], color="red", label="REPLAN")

# 🔥 tampilkan semua step di x-axis
plt.xticks(df["Step"], rotation=45)

plt.xlabel("Step")
plt.ylabel("Execution Time")
plt.title("Execution Time per Step")

# 🔥 log scale biar perbedaan kelihatan
plt.yscale("log")

# 🔥 grid (biar gampang baca)
plt.grid(True, which="both", linestyle="--", alpha=0.5)

plt.legend(loc="best")

plt.tight_layout()
plt.show()