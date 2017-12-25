import weakref
from MusicTheory.scale.ScaleKey import ScaleKey
from MusicTheory.scale.ScaleIntervals import ScaleIntervals
from MusicTheory.pitch.PitchClass import PitchClass
from MusicTheory.pitch.Key import Key
class Scale:
    def __init__(self, keyName='C', intervals=ScaleIntervals.Major):
        self.__ValidateInterval(intervals)
        self.__intervals = intervals
        self.__pitchClasses = []
        self.__names = []
        self.__scaleKey = None
        self.__scaleKey = ScaleKey(keyName, self)
        self.__calcPitchClasses()
        self.Key.Name = keyName

    @property
    def Key(self): return self.__scaleKey
    @property
    def Names(self): return self.__names

    @property
    def Intervals(self): return self.__intervals
    @Intervals.setter
    def Intervals(self, v):
        self.__ValidateInterval(v)
        self.__intervals = v
#        self.__calcPitchClasses()
        self.__Update()
    def __ValidateInterval(self, v):
        if not isinstance(v, (tuple, list)): raise TypeError(f'引数intervalsはtuple, listのいずれかにしてください。: type(v)={type(v)}')
        for i in v:
            if not isinstance(i, int): raise TypeError(f'引数intervalsの要素はint型にしてください。: type(i)={type(i)}')
            if i <= 0: raise ValueError(f'引数intervalsの要素は0より大きい整数値にしてください。: i={i}, v={v}')

    @property
    def PitchClasses(self): return self.__pitchClasses
    
    def GetPitchClass(self, degree:int):
        if not isinstance(degree, int): raise TypeError(f'引数degreeはint型にしてください。: type(degree)={type(degree)}')
        if degree < 1 or len(self.Intervals)+1 < degree: raise TypeError(f'引数degreeは音階の構成音数内の値にしてください。例えばMajorScaleは7音です。音度(degree)は1から始まるので1〜7までの整数値にしてください。: degree={degree}, self.Intervals={self.Intervals}, len(self.Intervals)={len(self.Intervals)}')
        return self.PitchClasses[degree-1]
    
    # ScaleKeyからも呼び出される
    def __Update(self, scaleKey=None):
        self.__calcPitchClasses(scaleKey)
        self.__calcNames()
    
    # 構成音のピッチクラスを算出する
    def __calcPitchClasses(self, scaleKey=None):
        key = scaleKey
        if None is not scaleKey and isinstance(scaleKey, ScaleKey): key = scaleKey
        else: key = self.Key
        self.__pitchClasses.clear()
        halfToneNum = key.PitchClass
        self.__pitchClasses.append(PitchClass.Get(halfToneNum))
        for i in self.__intervals:
            halfToneNum += i
            self.__pitchClasses.append(PitchClass.Get(halfToneNum))
    
    # 構成音のピッチクラスから音名を算出する
    def __calcNames(self):
        self.__names.clear()
#        self.__names.append(self.Key.Name)
        baseInterval = self.Key.PitchClass
        baseNames = self.__getBaseNames()
#        print('baseNames',baseNames)
#        baseNames = self.__getBaseNames(self.Key.PitchClass)
        for i,p in enumerate(self.PitchClasses):
#            print(self.__names)
            baseInterval += p[0]
            if p[0] in Key.PitchClasses: #構成音が幹音なら
                self.__names.append(Key.Keys[Key.PitchClasses.index(p[0])])
            else:
                if p[0] == Key.Get(baseNames[i] + '#'): self.__names.append(baseNames[i] + '#')
                elif p[0] == Key.Get(baseNames[i] + 'b'): self.__names.append(baseNames[i] + 'b')
                else: raise RuntimeError('音名を決められませんでした。アルゴリズムに問題があります。')
        
                """
                if self.Key.PitchClass in Key.PitchClasses: #調が幹音なら
                    if p[0] == Key.Get(baseNames[i] + '#'): self.__names.append(baseNames[i] + '#')
                    elif p[0] == Key.Get(baseNames[i] + 'b'): self.__names.append(baseNames[i] + 'b')
                    else: raise RuntimeError('音名を決められませんでした。アルゴリズムに問題があります。')
                else:
                    if p[0] == Key.Get(baseNames[i] + '#'): self.__names.append(baseNames[i] + '#')
                    elif p[0] == Key.Get(baseNames[i] + 'b'): self.__names.append(baseNames[i] + 'b')
                    else: raise RuntimeError('音名を決められませんでした。アルゴリズムに問題があります。')

#                    # 調の変化記号を優先する。次に変化記号なし、最後に調と異なる変化記号
#                    if self.Key.Name[1] in Accidental.Accidentals:

                        if -1 == Accidental.Accidentals[self.Key.Name[1]]: #♭の場合
                            if p[0] == Key.Get(baseNames[i] + 'b'): self.__names.append(baseNames[i] + 'b')
                            else: 
                            baseNames[i] + 'b'
                        elif 1 == Accidental.Accidentals[self.Key.Name[1]]: #♯の場合
                        else: raise RuntimeError(f'調の変化記号が不正です。次のいずれかにしてください。{Accidental.Accidentals}: self.Key.Name={self.Key.Name}')
                    if p[0] == Key.Get(baseNames[i] + '#'): self.__names.append(baseNames[i] + '#')
                    
                    
                    
                    pitch = PitchClass.Get(baseInterval)
                    
                    self.Key.PitchClass
                    startDegree = Key.Keys.index(self.Key.Name[0])
                    
                    if 7 < startDegree+i: startDegree+i-7
                    
                    self.__names.append(Key.Keys[Key.PitchClasses.index(p[0])])
                    
                
                
            if self.Key.PitchClass in Key.Keys: #調が幹音なら
            """
    
    #調を第1音にした音名リストを取得する（ただし変化記号はない）
#    def __getBaseNames(self, pitchClass):
    def __getBaseNames(self):
        names = []
        names.append(self.Key.Name[0])
        """
        names.append(self.Key.Name)
        start = -1
        if self.Key.PitchClass in Key.PitchClasses:
            start = Key.PitchClasses.index(self.Key.PitchClass)#p[0]
        else:
            for i,k in enumerate(Key.Keys):
                if self.Key.Name[0] == k:
                    start = i
                    break
#            start = self.Key.Name[0]
#        start = Key.PitchClasses.index(pitchClass)#p[0]
        if -1 == start: raise RuntimeError('調の音名が不正です。{Key.Keys}のいずれかにしてください。: self.Key.Name[0]={self.Key.Name[0]}')
        idx = start
        """
        idx = self.__getBaseNameStartIndex()
        for i in range(len(Key.Keys)*2):
#        for i in range(1, (len(Key.Keys)*2)-1):
            idx += 1
            idx = idx if idx < 7 else idx-7
#            print(f'i={i}, idx={idx}')
            names.append(Key.Keys[idx])
            if len(self.Intervals)+1 <= len(names): break
#        print('BN:', names)
        return names
        
    def __getBaseNameStartIndex(self):
        start = -1
        if self.Key.PitchClass in Key.PitchClasses:#調が幹音なら
            return Key.PitchClasses.index(self.Key.PitchClass)
        else:#調に変化記号があるなら
            return Key.Keys.index(self.Key.Name[0])
