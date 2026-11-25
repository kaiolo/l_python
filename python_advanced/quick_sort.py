def quick_sort(target,start,end):
    if start>=end:
        return
    left=start
    right=end
    mid=target[start]
    while left<right:
        while target[right]>=mid and left<right:
            right-=1
        target[left]=target[right]
        while target[left]<mid and left<right:
            left+=1
        target[right]=target[left]
        target[left]=mid
    quick_sort(target,start,left-1)
    quick_sort(target,right+1,end)

if __name__ =='__main__':
    target=[4,2,7,9,1,20,34,1,19,7,9]
    quick_sort(target,start=0,end=len(target)-1)
    print(target)
