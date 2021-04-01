

textCensor = ".."

def beep(content:str, word:list) -> str:

    for word in word:
        content = content.replace(word,textCensor)
    
    return content

if __name__ == "__main__":
    print(beep("sample text",["amp"]))
    print(beep("var/pro/1/yes/src.c",["var/pro","yes"]))

