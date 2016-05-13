program CatalogEntry
!
  implicit none
  character (len=511) :: line
  character (len=20) :: tCourse
  character (len=3) :: aformat = '(a)'
  integer :: i, ier, ndels, p(30)
!
  open(unit=1,file='catalog', status='old', form='formatted')
! open(unit=2,file='errors', status='replace', form='formatted')
  do 
    read(1,aformat,iostat=ier) line
    if (ier < 0) exit
    call GetPosDelimiters('|', line, ndels, p)
    tCourse = line(:p(1)-1)
    do i=2,len_trim(tCourse)-1
      if (tCourse(i:i) == ' ' .or. tCourse(i:i) == '.') tCourse(i:i) = '-'
    end do
    open (3, file=tCourse, status='replace', form='formatted')
    write(3,aformat) line(:p(1)-1), (adjustl(line(p(i)+1:p(i+1)-1)), i=1,ndels-1)
    close(3)
  end do
  close(1)
! close(2)
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

end program CatalogEntry
