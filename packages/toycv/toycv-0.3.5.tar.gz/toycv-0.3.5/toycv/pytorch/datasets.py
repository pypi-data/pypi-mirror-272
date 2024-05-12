from torch.utils.data import Dataset


class SubDataset(Dataset):
    def __init__(self, original_dataset, available_index_list=None):
        self.original_dataset = original_dataset
        self.available_index_list = [i for i in available_index_list if i < len(self.original_dataset)]

    def __len__(self):
        return len(self.available_index_list)

    def __getitem__(self, index):
        return self.original_dataset[self.available_index_list[index]]


class LimitedDataset(Dataset):
    def __init__(self, original_dataset, limit):
        self.original_dataset = original_dataset
        self.limit = limit

    def __len__(self):
        return min(len(self.original_dataset), self.limit)

    def __getitem__(self, index):
        if index >= self.limit:
            raise IndexError
        return self.original_dataset[index]
