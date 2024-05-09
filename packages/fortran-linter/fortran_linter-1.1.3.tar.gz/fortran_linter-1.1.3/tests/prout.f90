program test

    real :: start, finish

    integer, parameter :: N = 128
    integer :: i, j, k, Niter, iter

    real(kind=8), dimension(N, N, N) :: a, b

    Niter = 100
    call CPU_TIME(start)
    do iter = 1, Niter
        do i = 1, N
            do j = 1, N
                do k = 1, N
                    a(i, j, k) = i + j + k
                end do
            end do
        end do
    end do
    call CPU_TIME(finish)

    print*, "IJK took", finish - start, "seconds", maxval(a)

    call CPU_TIME(start)
    do iter = 1, Niter
        do i = 1, N
            do j = 1, N
                do k = 1, N
                    b(k, j, i) = i + j + k
                end do
            end do
        end do
    end do
    call CPU_TIME(finish)
    print*, "KJI took", finish - start, "seconds", maxval(b)
end program