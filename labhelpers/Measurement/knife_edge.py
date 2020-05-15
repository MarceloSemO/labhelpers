from labhelpers.Measurement.utils import init_file


def measure(step_mm, meas_func, zero_adjust_func, init_pos_mm=0.0, outfile=None):
    _adjust_zero(zero_adjust_func)
    f_out = init_file(outfile, ['Position (mm)', 'Power(W)'])

    curr_pos_mm = init_pos_mm
    while True:
        curr_pos_mm_str = "{:.2f}".format(curr_pos_mm)
        user_input = input("------------------------------------------\n"
                           "Next measurement at {} mm.\nPress 'Enter' to take next measurement. Enter 'q' and "
                           "press 'Enter' to finish measurement. Enter a number and press 'Enter' to set a new "
                           "step size. Enter 'del' and press 'Enter' to delete last measurement. \n"
                           .format(curr_pos_mm_str))
        try:
            new_step_mm = float(user_input)
            curr_pos_mm += new_step_mm - step_mm
            step_mm = new_step_mm
            print("Changed step size to ", round(step_mm, 2), "mm.")
            continue
        except ValueError:
            if user_input == '':
                meas_power_mW_str = meas_func
                print("Measured", meas_power_mW_str, " W.")
                if f_out is not None:
                    f_out.write("{}\t{:.5e}\n".format(curr_pos_mm_str, meas_power_mW_str))
                curr_pos_mm += step_mm
            elif user_input.lower() == 'q':
                if f_out is not None:
                    f_out.close()
                    print("Finished measurement. Saved file.")
                else:
                    print("Finshed Measurement.")
                break
            elif user_input.lower() == 'del':
                if f_out is not None:
                    f_out.seek(0)
                    lines = f_out.readlines()
                    f_out.seek(0)
                    f_out.truncate()
                    for line in lines[:-1]:
                        f_out.write(line)
                else:
                    print("No file for writing measurement given. Cannot delete from file.")
            else:
                print("No valid user input. Do nothing...")


def _adjust_zero(zero_adjust_func):
    input("Please prepare your setup for zero adjustment. "
          "Press Enter as soon as the setup is ready for zero adjustment.\n")
    zero_adjust_func()
