program Unique
!
  implicit none
  character (len=512) :: line1, line0
  character (len=3) :: aformat = '(a)'
  integer :: ier, ndels1, p1(30)
!
  open(unit=1,file='catalog', status='old', form='formatted')
  open(unit=2,file='catalog.new', status='new', form='formatted')
!
  line0 = '        '
  do 
    read(1,aformat,iostat=ier) line1
    if (ier < 0) exit
    call GetPosDelimiters('.', line1, ndels1, p1)
    if (line1(:p1(1)) /= line0(:p1(1))) write(2,aformat) trim(line1)
    line0 = line1
  end do
!
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

end program Unique
