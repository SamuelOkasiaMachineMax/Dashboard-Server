import re

def clean_serial(serial):
    # Remove all non-alphanumeric characters and then convert to upper case
    try:
        return re.sub(r'[^a-zA-Z0-9]', '', serial).upper()
    except:
        return serial

def is_potentially_same_serial(serial1, serial2, min_overlap=4):
    s1_clean = clean_serial(serial1)
    s2_clean = clean_serial(serial2)

    for i in range(min_overlap, len(s1_clean) + 1):
        segment = s1_clean[-i:]
        if segment in s2_clean:
            return True
    for i in range(min_overlap, len(s2_clean) + 1):
        segment = s2_clean[-i:]
        if segment in s1_clean:
            return True

    return False

def compare_eKey_to_eachKeyInPostman(eKey,postmanDict):

    for pKey in postmanDict.keys():
        if (is_potentially_same_serial(eKey,pKey)):
            return [eKey, pKey, postmanDict[pKey]['Source']]

def serialN(eKey, postmanDict):
    for pKey in postmanDict.keys():
        if eKey[-4:] == pKey[-4:]:
            return [eKey, pKey, postmanDict[pKey]['Source']]

def assetID(eKey,postmanDict,excelDict):

    for pKey in postmanDict.keys():
        try:
            same = postmanDict[pKey]['Equipment ID'] == excelDict[eKey]['AssetID']
        except:
            same = False
        try:
            similar = postmanDict[pKey]['Equipment ID'][-4:] == excelDict[eKey]['AssetID'][-4:]
        except:
            similar = False
        try:
            insideA = str(postmanDict[pKey]['Equipment ID']) in str(excelDict[eKey]['AssetID'])
        except:
            insideA = False
        try:
            insideB = str(excelDict[eKey]['AssetID']) in str(postmanDict[pKey]['Equipment ID'])
        except:
            insideB = False

        insideC = False

        for word in str(postmanDict[pKey]['Equipment ID']).split(' '):
            if word in str(excelDict[eKey]['AssetID']) and word.replace(' ','') != '' and word != '-' and len(word) >2 and word != 'NTD':
                insideC = True
        if insideC:
            pass
            # print(f"{'Postman Equipment ID:':<30} {postmanDict[pKey]['Equipment ID']}")
            # print(f"{'Excel Equipment ID:':<30} {excelDict[eKey]['AssetID']}")
            # print('\n')

        if (same or similar or insideA or insideB or insideC) and postmanDict[pKey]['Equipment ID'] != '':
            #print(postmanDict[pKey])
            #print('AssetID: '+ postmanDict[pKey]['Equipment ID']+' Excel Assset ID: ', excelDict[eKey]['AssetID'], postmanDict[pKey]['Source'])≥9
            #return [eKey, pKey, postmanDict[pKey]['Source'],excelDict[eKey]['AssetID'],postmanDict[pKey]['Equipment ID']]
            return {
                    'Serial Platform': eKey, 'Serial Postman': pKey,
                    'Asset ID Platform': excelDict[eKey]['AssetID'], 'Asset ID Postman':postmanDict[pKey]['Equipment ID'],
                    'Source': postmanDict[pKey]['Source']
                 }



def main(excelDict,postmanDict):

    possible_matches = []
    count = 0
    for eKey in excelDict.keys():
        # try:
        #
        #     outcome = serialN(eKey, postmanDict)
        #     if outcome:
        #         possible_matches.append(outcome + [excelDict[eKey]['AssetID']])
        #
        # except:
        #     pass


        try:

            outcome2 = assetID(eKey, postmanDict, excelDict)
            if outcome2:
                possible_matches.append(outcome2)

        except Exception as E:
            pass

        '''
            count = +1
        if count ==1:
            serialN(eKey,postmanDict)
        '''


        '''      
        try:
            outcome = compare_eKey_to_eachKeyInPostman(eKey,postmanDict)
            if outcome:
                possible_matches.append(outcome+[excelDict[eKey]['AssetID']])
                print(outcome+[excelDict[eKey]['AssetID']])
        except:
            pass
        '''

    return possible_matches




