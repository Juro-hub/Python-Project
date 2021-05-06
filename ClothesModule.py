# info_list의 요소는 리스트 [url, like count, jpg file]이다
# 리스트를 요소로 갖는 리스트가 info_list
class Clothes:
    def __init__(self, file_name):
        self.info_list = []
        self.index = 0 # 베스트 좋아요 index
        self.Load(file_name)

    def Load(self, file_name):
        self.info_list.clear()

        # 파일 읽기
        try:
            file = open(file_name, mode='rt', encoding='utf-8')    
        except FileNotFoundError:  # 파일이 존재하지 않으면
           print("%s이 없습니다." % file_name)  
        else:
            read_list = file.readlines() # 파일의 모든 라인을 list로 받는다
            file.close()

        i = 0
        # 각 라인의 url, like count, jpg file을 여백으로 나눈다
        for line in read_list:
            line = line.rstrip("\n") # 엔터 제거        
            line_list = line.split(' ') # 여백으로 구분된 문자열 리스트
            if len(line_list) == 1: # url만 있으면
                # like count가 없으면 0으로 추가
                line_list.append(0)            
                # jpg 이미지 파일 추가
                img_file = "{0}.jpg".format(i+1)
                line_list.append(img_file)
            else:
                line_list[1] = int(line_list[1]) # like count는 숫자로 바꾼다
            i += 1
            self.info_list.append(line_list)
        #print(info_list)
        #print()       
        # like count로 내림 차순 정렬
        self.info_list = sorted(self.info_list, key=lambda line_list: line_list[1], reverse=True)  
        print(self.info_list)

    def GetBestList(self):
        best_list = self.info_list[self.index]                
        return best_list

    # 싫어요를 눌렀을때
    def DisLike(self):
        self.index = (self.index + 1) % len(self.info_list) # 0 ~ max을 반복하도록 나머지 연산

    # 좋아요를 눌렀을때
    def Like(self):
        best_list = self.GetBestList()
        best_list[1] += 1

    def Save(self, file_name):        
        file = open(file_name, mode='wt', encoding='utf-8')    
        for line in self.info_list:
            line[1] = str(line[1])
            line_str = "{0} {1} {2}\n".format(line[0], line[1], line[2])
            file.write(line_str)             
        file.close()




#    def Sort(self):
if __name__ == '__main__':    
    info_list = []

    info_list.clear()

    file_name = "./이미지/여자/10도이하/0.txt"

    # 파일 읽기
    try:
        file = open(file_name, mode='rt', encoding='utf-8')    
    except FileNotFoundError:  # 파일이 존재하지 않으면
        print("%s이 없습니다." % file_name)  
    else:
        read_list = file.readlines() # 파일의 모든 라인을 list로 받는다
        file.close()

    i = 0
    # 각 라인의 url, like count, jpg file을 여백으로 나눈다
    for line in read_list:
        line = line.rstrip("\n") # 엔터 제거        
        line_list = line.split(' ') # 여백으로 구분된 문자열 리스트
        if len(line_list) == 1: # like count가 없으면 0으로 추가
            # like count가 없으면 0으로 추가
            line_list.append(0)            
            # jpg 이미지 파일 추가
            img_file = "{0}.jpg".format(i+1)
            line_list.append(img_file)
        else:
            line_list[1] = int(line_list[1]) # like count는 숫자로 바꾼다        
        i += 1
        info_list.append(line_list)

    print(info_list)
    print()
       
    # like count로 내림 차순 정렬
    info_list = sorted(info_list, key=lambda line_list: line_list[1], reverse=True)  

    print(info_list)

    # 파일 쓰기
    file_name = './이미지/여자/10도이하/t.txt'
    file = open(file_name, mode='wt', encoding='utf-8')    
    for line in info_list:
        line[1] = str(line[1])
        line_str = "{0} {1} {2}\n".format(line[0], line[1], line[2])
        file.write(line_str)             
    file.close()
