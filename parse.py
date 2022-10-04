
DEBUG_1=False
import csv
class instruction:
    def __init__(self,op:int,f3:int,f7:int,t:str,i:int):
        self.rs1 = None
        self.rs2 = None
        self.rd = None
        self.op = op
        self.f3 = f3
        self.f7 = f7
        self.t = t 
        self.i = i
    def __str__(self) -> str:
        return f"{self.op}, {self.f3}, {self.f7}, {self.t}, {self.i}"
def init_instructions():
    d = {}
    with open("RISC-V_Instructions.csv", 'r') as file:
        r = csv.reader(file)
        first = True

        for l in r:
            if first: 
                first = False
                continue
            d[l[0]] = instruction(l[1],l[2],l[3],l[4],l[5])
            # print(l)
    # for k in d.keys():
    #     print(k, d[k])
    return d

def get_bin_str(x:int,l:int)->str:
    if x >= 0:
        f = "0"
        si = 2
    else:
        si = 3
        f = "1"
    return (bin(x))[si:].rjust(l,f)

def formatBinStr(arr:list,d:dict):
    
    inst = d[arr[0]]
    if arr[0] == "ebreak":
        return "00000000000100000000000001110011"
    if arr[0] == "ecall":
        return "00000000000000000000000001110011"
    if inst.t == "R":
        rs1_str = get_bin_str(int((arr[2])[1:]),5)
        
        rs2_str = get_bin_str(int((arr[3])[1:]),5)
        
        rd_str = get_bin_str(int((arr[1])[1:]),5)

        return f"{inst.f7}{rs2_str}{rs1_str}{inst.f3}{rd_str}{inst.op}"
    if inst.t == "I":
        temp = []
        imm = ""
        for i in range(1,len(arr)):
            if arr[i].startswith("x"):
                temp.append(arr[i])
            else:
                imm = arr[i]
        rs1_str = get_bin_str(int((temp[1])[1:]),5)
        rd_str = get_bin_str(int((temp[0])[1:]),5)
        imm = get_bin_str(int(imm),12)
        # pass
        return f"{imm}{rs1_str}{inst.f3}{rd_str}{inst.op}"
    if inst.t == "S":
        
        pass
    if inst.t == "B":
        
        pass
    if inst.t == "U":
        
        pass
    if inst.t == "J":
        
        pass
    
    return "instruction not recognized or supported"

def run_tests():
    skip = []
    d = init_instructions()
    with open("./lab3_unit_tests_2.csv","r") as tests:
        reader = csv.reader(tests,delimiter="|")
        p = 0
        f = 0 
        i = 0
        for test in reader:
            i+=1
            if i in skip:
                continue
            print("test ",i)
            print("enter an instruction:")
            print(test[0])
            inst = test[0]
            inst = inst.replace(","," ")
            inst = inst.replace("("," ")
            inst = inst.replace(")","")
            arr = inst.split()
            print(arr)
            res = formatBinStr(arr,d)
            print("Expect:",test[1])
            print("Actual:",res)
            if res == test[1]:
                print("PASS ✅")
                p+=1
            else:
                f+=1
                print("FAIL ❌")
        print("total passed:",p)
        print("total failed:",f)
    return
def main():
    if DEBUG_1:
        d = init_instructions()
        inst = input("Enter an Instruction: ")
        inst = inst.replace(","," ")
        inst = inst.replace("("," ")
        inst = inst.replace(")","")
        arr = inst.split()
        print(arr)
        print(formatBinStr(arr,d))
        return
    run_tests()
    # print(bin(4)[2:])
    return

main()