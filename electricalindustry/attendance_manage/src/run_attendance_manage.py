if __name__ == '__main__':
    import sys
    from attendance_manage.start import main

    debug_flag = True
    if len(sys.argv) == 2:
        if sys.argv[1] == 'product':
            debug_flag = False

    main(debug_flag)