import logging
import torch
from tqdm import tqdm
from datasets import Dataset
from transformers import AutoModelForTokenClassification
from copy import deepcopy
from torcheval.metrics.functional import multiclass_f1_score, multiclass_confusion_matrix, binary_f1_score
from IPython.display import clear_output
from torch.utils.data import DataLoader

class ClassbiteTrainer:
    """
    A class to facilitate training and evaluation of a token classification model.

    Args:
        model (AutoModelForTokenClassification): The token classification model to be trained.
        optimizer (torch.optim): The optimizer used for training.
        n_classes (int): The number of classes for token classification.
        device (str, optional): The device where the model will be trained. Defaults to "cuda".

    Methods:
        compile(train_dataloader, validation_dataloader, n_epochs=20):
            Train and validate the token classification model.

    Attributes:
        history (list): List to store the evaluation metric (F1-score) history during training.
        best_model (AutoModelForTokenClassification): The best-performing model based on validation F1-score.
    """

    def __init__(
        self,
        model : AutoModelForTokenClassification,
        optimizer : torch.optim,
        n_classes : int ,
        device : str = "cuda",
    ) -> None:
        """
        Initialize ClassBite with the provided token classification model, optimizer, and other parameters.

        Args:
            model (AutoModelForTokenClassification): The token classification model to be trained.
            optimizer (torch.optim): The optimizer used for training.
            n_classes (int): The number of classes for token classification.
            device (str, optional): The device where the model will be trained. Defaults to "cuda".
        """
        self.model = model
        self.device = device
        self.optimizer = optimizer 
        self.n_classes = n_classes


    def train(
        self,
        train_dataloader : Dataset,
        validation_dataloader : Dataset,
        n_epochs : int = 20
    ):
        """
        Train and validate the token classification model.

        Args:
            train_dataloader (Dataset): DataLoader containing the training data.
            validation_dataloader (Dataset): DataLoader containing the validation data.
            n_epochs (int, optional): Number of epochs for training. Defaults to 20.

        Returns:
            list: History of evaluation metric (F1-score) during training.
        """
        self.history = []
        self.model.train()
        best_f1 = 0
        self.best_model = None

        for epoch in tqdm(range(n_epochs)):
            for batch in (train_dataloader):
                for k,v in batch.items():
                    batch[k] = v.to(self.device)

                    if k == "bbox":
                        continue
                    batch[k] = batch[k].reshape(1,512)
                batch.pop('bbox')

                self.optimizer.zero_grad()

                out = self.model(**batch)
                loss = out.loss

                loss.backward()
                self.optimizer.step()

            y_pred_val = torch.tensor([],device=self.device)
            y_true_val = torch.tensor([],device=self.device)

            for batch in validation_dataloader:
                for k,v in batch.items():
                    batch[k] = v.to(self.device)

                    if k == "bbox":
                        continue
                    batch[k] = batch[k].reshape(self.n_classes,512)
                batch.pop('bbox')

                y_true = batch['labels']
                mask = y_true!= -100

                with torch.no_grad():
                    y_pred = self.model(**batch).logits[:,:,1]
                y_pred = y_pred[mask]\
                    .reshape(self.n_classes,-1)[:,1:]\
                    .argmax(dim = 0)

                y_true = y_true[mask]\
                    .reshape(self.n_classes,-1)[:, 1:]\
                    .argmax(dim = 0)
                
                y_pred_val = torch.cat([y_pred, y_pred_val])
                y_true_val = torch.cat([y_true, y_true_val])

            if self.n_classes == 2:
                f1 = binary_f1_score(
                    y_pred_val,
                    y_true_val,
                )

            else:

                f1 = multiclass_f1_score(
                    y_pred_val,
                    y_true_val,
                    num_classes=self.n_classes
                )

            self.history.append(f1.item())

            conf_matrix = multiclass_confusion_matrix(
                y_true_val.to(torch.int64),
                y_pred_val.to(torch.int64),
                num_classes= self.n_classes
            )

            clear_output(True)
            print(f'f1-score : {f1.item()}')
            print(conf_matrix)
            

            if f1 > best_f1:
                best_f1 = f1
                self.best_model = deepcopy(self.model)

            logging.info(f"f1 score: {f1}")
            logging.info(conf_matrix)

        return self.history
    
    def test(
        self,
        test_dataloader : DataLoader
    ):
        """
        Performs testing on the provided test dataloader.

        Args:
            test_dataloader (DataLoader): The dataloader containing the test dataset.

        Returns:
            Tuple[torch.Tensor, torch.Tensor]: A tuple containing the true labels and predicted labels.
        """
        y_pred_test = torch.tensor([],device=self.device)
        y_true_test = torch.tensor([],device=self.device)
        with torch.no_grad:
            for batch in tqdm(test_dataloader):
                for k,v in batch.items():
                    batch[k] = v.to(self.device)

                    if k == "bbox":
                        continue
                    batch[k] = batch[k].reshape(4,512)
                batch.pop('bbox')

                y_true = batch['labels']
                mask = y_true!= -100

                with torch.no_grad():
                    y_pred = self.best_model(**batch).logits[:,:,1]
                y_pred = y_pred[mask]\
                    .reshape(self.n_classes,-1)[:,1:]\
                    .argmax(dim = 0)

                y_true = y_true[mask]\
                    .reshape(self.n_classes,-1)[:, 1:]\
                    .argmax(dim = 0)
                
                y_pred_test = torch.cat([y_pred, y_pred_test])
                y_true_test = torch.cat([y_true, y_true_test])

            return y_true_test, y_pred_test

