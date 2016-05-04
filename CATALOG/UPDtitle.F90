program AmendList
!
! amends masterfile with updatefile to produce new masterfile
!
  implicit none
  character (len=256) :: line1, line2, MSTfile, UPDfile, NEWfile, DIFFfile
  character (len=127) :: title
  character (len=3) :: aformat = '(a)'
  integer :: i, ier, ndels1, ndels2, p1(30), p2(30)
  logical :: fileOK, done1, done2
!
! write(*,*) 'Master file : '
! read(*,aformat) MSTfile
  MSTfile = 'courses.old'
  inquire(file=MSTfile, exist=fileOK)
  if (.not. fileOK) then
    write(*,*) 'File not found : '//trim(MSTfile)
    stop
  end if
!
! write(*,*) 'Update file : '
! read(*,aformat) UPDfile
  UPDfile = 'titles.csv' 
  inquire(file=UPDfile, exist=fileOK)
  if (.not. fileOK) then
    write(*,*) 'File not found : '//trim(UPDfile)
    stop
  end if
!
! write(*,*) 'New master file : '
! read(*,aformat) NEWfile
  NEWfile = 'courses'
  open(unit=3,file=NEWfile, status='replace', form='formatted')
!
  DIFFfile = 'notused'
  open(unit=4,file=DIFFfile, status='replace', form='formatted')
!
  open(unit=1,file=MSTfile, status='old', form='formatted')
  read(1,aformat) line1
  call GetPosDelimiters(',', line1, ndels1, p1)
  done1 = .false.
!
  open(unit=2,file=UPDfile, status='old', form='formatted')
  read(2,aformat) line2
  call GetPosDelimiters(',', line2, ndels2, p2)
  done2 = .false.
!
  do while (.not. done1 .and. .not. done2)
    if (line1(:p1(1)) < line2(:p2(1))) then ! no entry in update file
!     write(4,aformat) trim(line1)
! place prereq before title
      write(3,aformat) line1(:p1(11))//trim(line1(p1(12)+1:))//line1(p1(11):p1(12)-1)
      do
        read(1,aformat,iostat=ier) line1
        if (ier < 0) exit
        if (line1(1:1) /= '#') exit
      end do
      if (ier < 0) then
        done1 = .true.
      else
        call GetPosDelimiters(',', line1, ndels1, p1)
      end if
    else if (line1(:p1(1)) > line2(:p2(1))) then ! no entry in master file
      write(4,aformat) trim(line2)
      read(2,aformat,iostat=ier) line2
      if (ier < 0) then
        done2 = .true.
      else
        call GetPosDelimiters(',', line2, ndels2, p2)
      end if
    else
! match
! ABM 103,DABM,3,12,0,3,25,25,0,0,0,INTRO TO AGRIBUSINESS MGT,MGT 151
!        1    2 3  4 5 6  7  8 9 0 1                         2
! place prereq before title
      title = line1(p1(11)+1:p1(12)-1)
      if (title(1:1) == '(') then
        i = index(title, ')')
        write(*,*) 'prefixing '//title(:i)
        write(3,aformat) line1(:p1(11))//trim(line1(p1(12)+1:))//','//title(1:i)// &
          ' '//trim(line2(p2(1)+1:))
      else
        write(3,aformat) line1(:p1(11))//trim(line1(p1(12)+1:))//trim(line2(p2(1):))
      end if
!
      read(1,aformat,iostat=ier) line1
      if (ier < 0) then
        done1 = .true.
      else
        call GetPosDelimiters(',', line1, ndels1, p1)
      end if
!
      read(2,aformat,iostat=ier) line2
      if (ier < 0) then
        done2 = .true.
      else
        call GetPosDelimiters(',', line2, ndels2, p2)
      end if
    end if
  end do
!
  do while (.not. done1)
    write(3,aformat) trim(line1)
    read(1,aformat,iostat=ier) line1
    if (ier < 0) done1 = .true.
  end do
  do while (.not. done2)
    write(4,aformat) trim(line2)
    read(2,aformat,iostat=ier) line2
    if (ier < 0) done2 = .true.
  end do
!
  close(1)
  close(2)
  close(3)
  close(4)
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

end program AmendList
