#from MusicTheory.scale.Scale import Scale
import MusicTheory.scale.Scale
from MusicTheory.scale.ScaleIntervals import ScaleIntervals
#from MusicTheory.pitch.PitchClass import PitchClass
#from MusicTheory.pitch.OctaveClass import OctaveClass
#from Framework.ConstMeta import ConstMeta
from MusicTheory.pitch.PitchClass import PitchClass
from MusicTheory.pitch.Key import Key

#Scaleの内部クラスとして利用される。ScaleKeyクラス自体単独で使われることはない。むしろ使えない。
#変化記号がないと音階構成音の音名が定められない。よってピッチクラスでなく音名(Key)で取得する。
class ScaleKey:
    def __init__(self, name='C', scale=None):
        self.__pitchClass = -1
#        self.__name = None
        self.__name = name
        if not isinstance(scale, MusicTheory.scale.Scale.Scale): raise TypeError(f'引数scaleはScale型にしてください。: type(scale)={type(scale)}')
        self.__scale = scale
#        self.Name = name
    @property
    def Name(self): return self.__name
    @Name.setter
    def Name(self, v):
        self.__pitchClass = PitchClass.Get(Key.Get(v))[0]
        self.__name = v
        self.__scale._Scale__Update(self)
#        self.__scale._Scale__calcPitchClasses(self)
    @property
    def PitchClass(self): return self.__pitchClass

