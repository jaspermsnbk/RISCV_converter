
import sys
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
    with open("./RISC-V_Instructions.csv", 'r') as file:
        r = csv.reader(file)
        first = True

        for l in r:
            if first: 
                first = False
                continue
            d[l[0]] = instruction(l[1],l[2],l[3],l[4],l[5])
    return d

def get_bin_str(x:int,l:int)->str:
    if x >= 0:
        f = "0"
        si = 2
    else:
        si = 3
        f = "1"
    return (bin(x))[si:].rjust(l,f)

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is

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
        temp = []
        imm = ""
        for i in range(1,len(arr)):
            if arr[i].startswith("x"):
                temp.append(arr[i])
            else:
                imm = arr[i]
        r1 = get_bin_str(int((temp[1])[1:]),5)
        r2 = get_bin_str(int((temp[0])[1:]),5)
        imm = get_bin_str(int(imm),12)
        imm_upper = imm[0:7]
        imm_lower = imm[7:]
        return f"{imm_upper}{r2}{r1}{inst.f3}{imm_lower}{inst.op}"
    if inst.t == "B":
        temp = []
        imm = ""
        for i in range(1,len(arr)):
            if arr[i].startswith("x"):
                temp.append(arr[i])
            else:
                imm = arr[i]
        r1 = get_bin_str(int((temp[0])[1:]),5)
        r2 = get_bin_str(int((temp[1])[1:]),5)
        imm = get_bin_str(int(imm),13)
        imm_upper = imm[0]+imm[2:8]
        imm_lower = imm[9:]+imm[1]
        print("imm_upper:",imm_upper)
        print("r2:",r2)
        print("r1:",r1)
        print("inst.f3:",inst.f3)
        print("imm_lower:",imm_lower)
        print("imm:",inst.op)

        return f"{imm_upper}{r2}{r1}{inst.f3}{imm_lower}{inst.op}"
    if inst.t == "U":
        temp = []
        imm = ""
        for i in range(1,len(arr)):
            if arr[i].startswith("x"):
                temp.append(arr[i])
            else:
                imm = arr[i]
        imm_upper = get_bin_str(int(imm),20)
        rd_str = get_bin_str(int(temp[0][1:]),5)
        return f"{imm_upper}{rd_str}{inst.op}"
    if inst.t == "J":
        temp = []
        imm = "0"
        for i in range(1,len(arr)):
            if arr[i].startswith("x"):
                temp.append(arr[i])
            else:
                imm = arr[i]
            
            imm_temp = get_bin_str(int(imm),32)
            imm_temp = imm_temp[-32:-12]
            rd_str = get_bin_str(int(temp[0][1:]),5)
            imm_tot = f"{imm_temp[-20]}{imm_temp[-10:]}{imm_temp[-11]}{imm_temp[-19:-11]}"
        return f"{imm_tot}{rd_str}{inst.op}"
    
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
            print("inst type: ", d[arr[0]].t)
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
    if len(sys.argv) > 1 and sys.argv[1] == "-u":
        run_tests()
        return
    d = init_instructions()
    inst = input("Enter an Instruction: ")
    inst = inst.replace(","," ")
    inst = inst.replace("("," ")
    inst = inst.replace(")","")
    arr = inst.split()
    print(arr)
    print(formatBinStr(arr,d))
    return
main()