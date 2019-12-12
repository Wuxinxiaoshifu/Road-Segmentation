import torch
import torch.nn as nn
import torch.utils.data as data
import torch.optim as optim
import models
from datasets import RoadsDatasetTrain


# temp values
MODEL = models.fcn_resnet101
EPOCHS = 100
LEARNING_RATE = 0.0001
BATCH_SIZE = 1
CRITERION = nn.BCELoss()
# we have 2 classes
OUTPUT_CHANNELS = 2



def train(model, dataloader, epochs, criterion, model_weights=None):

    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    for epoch in range(epochs):
        model.train()
        for ind_batch, sample_batched in enumerate(dataloader):
            batch_images = sample_batched["image"]
            batch_groundtruth = sample_batched["groundtruth"]
            
            optimizer.zero_grad()

            output = model(batch_images)
            
            loss = criterion(
                output,
                batch_groundtruth
            )
            
            loss.require_grad = True
            loss.backward()
            
            optimizer.step()

            if ind_batch % 10 == 0:
                print(
                    "[Epoch {}, Batch {}/{}]:  [Loss: {:03.2f}]".format(
                        epoch, ind_batch, len(dataloader), loss
                    )
                )

if __name__ == "__main__":
    # TODO: model
    model = MODEL
    data_dir = "./Datasets/training"
    dataset = RoadsDatasetTrain(root_dir=data_dir)
    dataloader = data.DataLoader(dataset=dataset, batch_size=BATCH_SIZE, shuffle=True)
    train(model=model, dataloader=dataloader, epochs=EPOCHS, criterion=CRITERION)
