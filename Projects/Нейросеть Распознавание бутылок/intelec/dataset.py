from pathlib import Path

train_path = Path("dataset/images/train")
val_path = Path("dataset/images/val")

print("Train images:", list(train_path.glob("*.jpg")))
print("Val images:", list(val_path.glob("*.jpg")))
