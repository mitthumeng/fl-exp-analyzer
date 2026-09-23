import os
import matplotlib.pyplot as plt


def plot_metrics(records, output_dir="results"):
    if not records:
        return

    os.makedirs(output_dir, exist_ok=True)

    rounds = [x["round"] for x in records]
    accuracies = [x["accuracy"] for x in records]
    losses = [x["loss"] for x in records]

    plt.figure()
    plt.plot(rounds, accuracies, marker="o")
    plt.xlabel("Round")
    plt.ylabel("Accuracy")
    plt.title("Accuracy over Training Rounds")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "accuracy_curve.png"))
    plt.close()

    plt.figure()
    plt.plot(rounds, losses, marker="o")
    plt.xlabel("Round")
    plt.ylabel("Loss")
    plt.title("Loss over Training Rounds")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "loss_curve.png"))
    plt.close()