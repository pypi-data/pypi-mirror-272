#MLP means Machine Learning Pictures
#PIXEON: Picture Exploration & Neural Training Module
#Author: Logan McDermott
#Date: 5/3/2024


#imports
from time import sleep


class Picture:
  def __init__(self, filepath: str, MLP: str | list[str]):
    self.filepath = filepath
    self.MLP = MLP
    
  def accuratize(self):
    score = 0
    with open(self.filepath, 'rb') as f1, open(self.MLP, 'rb') as f2:
      content1 = f1.read()
      content2 = f2.read()
      min_len = min(len(content1), len(content2))
      for i in range(min_len):
        if content1[i] == content2[i]:
          score += 1
      accuracy = score / min_len if min_len > 0 else 0
      return score, accuracy


  def config(self, filepath=None, MLP=None):
    #picture or MLP
    if filepath:
      self.filepath = filepath
    elif MLP:
      self.MLP = MLP
    else:
      raise (ValueError, "No value was modified")
  def catagorize(self):
    #returns the average of bulk photos, only works if the MLP
    #arg in the Picture class is a list
    og_mlp = self.MLP
    acc_list = []
    #calculate accuracy in all files
    for picture in self.MLP:
      self.config(MLP=picture)
      _, acc = self.accuratize()
      acc_list.append(acc)
    #avg it
    avg = sum(acc_list) / len(acc_list)
    #reset Machine Learning Path/Picture
    self.config(MLP=og_mlp)
    return avg
