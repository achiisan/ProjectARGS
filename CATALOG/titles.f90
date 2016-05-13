program ExtractTitles
!
  implicit none
  character (len=511) :: line
  character (len=127) :: title
  character (len=20) :: tCourse
  character (len=3) :: aformat = '(a)'
  integer :: ier, ndels, p(30)
!
  open(unit=1,file='catalog', status='old', form='formatted')
  open(unit=2,file='titles.csv', status='replace', form='formatted')
!
  do 
    read(1,aformat,iostat=ier) line
    if (ier < 0) exit
    call GetPosDelimiters('.', line, ndels, p)
    if (line(p(1)+1:p(1)+1) == '1') then
      write(*,*) line(:p(2)-1)//': delimiter in course code'
      p(1) = p(2)
      p(2) = p(3)
    end if
    tCourse = line(:p(1)-1)
    title = line(p(1)+1:p(2)-1)
    ndels = index(title, '(')
    if (ndels > 0) then
      write(2,aformat) trim(tCourse)//','//adjustl(title(:ndels-1))
    else
      write(*,*) trim(tCourse)//' has no units ?'
    end if
  end do
  close(1)
  close(2)
!
  write(*,*) 'Bye!'
  stop

  contains

    subroutine GetPosDelimiters(delim, textline, ndelims, pos)
      character (len=1), intent (in) :: delim
      character (len=*), intent (in) :: textline
      integer, intent (out) :: ndelims
      integer, dimension(:), intent (out) :: pos
      integer :: j, k
!
      ndelims = 0
      pos = 0
      k = len_trim(textline)
      do j=1,k
        if (textline(j:j) == delim) then
          ndelims = ndelims+1
          pos(ndelims) = j
        end if
      end do
      ndelims = ndelims+1
      pos(ndelims) = k+1
      return
    end subroutine GetPosDelimiters

end program ExtractTitles
