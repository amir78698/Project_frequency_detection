
# importing required libraries

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from torchvision import datasets, models, transforms
import time

# creating function for training

def train_model(model, criterion, optimizer, scheduler,model_path, num_epochs=25):
    """
    function to train the Deep Neural Network and save the model to use for inference
    """
    since = time.time()

    best_acc = 0.0

    for epoch in range(num_epochs):
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 10)

        model.train()  # Set model to training mode

        running_loss = 0.0
        running_corrects = 0

        # Iterate over data.
        for inputs, labels in dataloader:
            inputs = inputs.to(device)
            labels = labels.to(device)

            # zero the parameter gradients
            optimizer.zero_grad()

            # track history for training
            with torch.set_grad_enabled(True):
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = criterion(outputs, labels)

                # backward + optimize
                loss.backward()
                optimizer.step()

            # statistics
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
            scheduler.step()

        epoch_loss = running_loss / dataset_size
        epoch_acc = running_corrects.double() / dataset_size

        print('Loss: {:.4f} Acc: {:.4f}'.format(
             epoch_loss, epoch_acc))

        best_acc = epoch_acc

        #model_path = "DNN/trained_model.pth"
        torch.save(model.state_dict(), model_path)

        print()

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))
    print('Best training Acc: {:4f}'.format(best_acc))

    print("model has been saved in {}".format(model_path))


if __name__ == "__main__":

    # Data augmentation and normalization for training
    data_transforms = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

    data_dir = "/media/amir/EAFC6F14FC6ED9F9/IDMT/dataset/cropped_img"
    image_dataset = datasets.ImageFolder(data_dir, data_transforms)
    dataloader = torch.utils.data.DataLoader(image_dataset, batch_size=4, shuffle=True, num_workers=4)
    dataset_size = len(image_dataset)
    class_names = image_dataset.classes

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # loading model for fine tuning
    model_ft = models.resnet18(pretrained=True)
    num_ftrs = model_ft.fc.in_features

    # Here the size of each output sample is set to 4.
    model_ft.fc = nn.Linear(num_ftrs, 4)

    model_ft = model_ft.to(device)

    criterion = nn.CrossEntropyLoss()

    # Observe that all parameters are being optimized
    optimizer_ft = optim.SGD(model_ft.parameters(), lr=0.001, momentum=0.9)

    # Decay LR by a factor of 0.1 every 7 epochs
    exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=7, gamma=0.1)

    # path to save model
    model_path = "/media/amir/EAFC6F14FC6ED9F9/IDMT/dataset/model.pth"

    # Calling function to start training
    train_model(model_ft, criterion, optimizer_ft, exp_lr_scheduler, model_path, num_epochs=25)
