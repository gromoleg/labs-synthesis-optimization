import sys
import constants
import logging
import operator
from . import parser
from threading import Event

py2 = sys.version_info[0] == 2
if py2:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
else:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *


class Method(QWidget):
    solution_pause_signal = pyqtSignal()
    solution_resume_signal = pyqtSignal(int)
    solution_return_signal = pyqtSignal(dict)
    solution_stop_signal = pyqtSignal()

    def __init__(self, solution_class):
        super(Method, self).__init__()
        self.layout = QVBoxLayout()
        for param in self.params:
            name = param.get('name', param['var_name'])
            if 'type' not in param:
                param['type'] = constants.default_p_type
            type_ = param['type']
            if type_ in constants.p_aliases:
                param['type'] = type_ = constants.p_aliases[type_]
            value = param.get('default', getattr(constants, param['var_name'], ''))
            label = QLabel('%s:' % name)
            text_edit = QTextEdit()
            text_edit.setMaximumHeight(text_edit.document().size().toSize().height() + 2)
            text_edit.setText(str(value))
            label.setBuddy(text_edit)
            h_layout = QHBoxLayout()
            h_layout.addWidget(label)
            h_layout.addWidget(text_edit)
            self.layout.addLayout(h_layout)
            param['qt_input'] = text_edit
        self.result_label = QLabel()
        self.result_label.setVisible(False)
        self.layout.addWidget(self.result_label)

        self.solution_table = SolutionTable()
        self.solution_table.setVisible(False)
        self.layout.addWidget(self.solution_table)

        h_layout = QHBoxLayout()

        self.btn_solve = QPushButton('Solve')
        self.btn_solve.clicked.connect(lambda: self.btn_solve_clicked())

        self.btn_pause_resume = QPushButton('Pause')
        self.btn_pause_resume.setVisible(False)
        self.btn_pause_resume.clicked.connect(lambda: self.btn_pause_resume_clicked())

        self.btn_steps = QPushButton('Steps')
        self.btn_steps.clicked.connect(lambda: self.btn_steps_clicked())

        self.btn_prev_step = QPushButton('Previous step')
        self.btn_prev_step.setVisible(False)
        self.btn_prev_step.clicked.connect(lambda: self.btn_prev_step_clicked())

        self.btn_next_step = QPushButton('Next step')
        self.btn_next_step.setVisible(False)
        self.btn_next_step.clicked.connect(lambda: self.btn_next_step_clicked())

        self.btn_stop = QPushButton('Stop')
        self.btn_stop.setVisible(False)
        self.btn_stop.clicked.connect(lambda: self.btn_stop_clicked())

        h_layout.addWidget(self.btn_solve)
        h_layout.addWidget(self.btn_pause_resume)
        h_layout.addWidget(self.btn_steps)
        h_layout.addWidget(self.btn_prev_step)
        h_layout.addWidget(self.btn_next_step)
        h_layout.addWidget(self.btn_stop)
        self.layout.addLayout(h_layout)

        self.solution_class = solution_class
        self.solution_return_signal.connect(self.proceed_solution)
        self.solution_thread = None
        self.solution_event = Event()
        self.solution_steps = []
        self.solution_current_step = 0
        self.is_paused = False
        self.is_steps = False

        self.setLayout(self.layout)

    def btn_solve_clicked(self):
        if self.solution_thread and self.solution_thread.isRunning():
            return
        self.is_steps = False
        self.btn_solve.setVisible(False)
        self.btn_pause_resume.setVisible(True)
        self.btn_steps.setVisible(False)
        self.btn_prev_step.setVisible(False)
        self.btn_next_step.setVisible(False)
        self.btn_stop.setVisible(True)
        self.start_solution()

    def btn_pause_resume_clicked(self):
        if self.is_paused:
            self.btn_pause_resume.setText('Pause')
            self.btn_prev_step.setVisible(False)
            self.btn_next_step.setVisible(False)
            self.resume_solution()
        else:
            self.btn_pause_resume.setText('Resume')
            self.btn_prev_step.setVisible(True)
            self.btn_next_step.setVisible(True)
            self.pause_solution()
        self.is_paused = not self.is_paused
        self.btn_pause_resume.setVisible(True)

    def btn_steps_clicked(self):
        if self.solution_thread and self.solution_thread.isRunning():
            return
        self.is_steps = True
        self.btn_solve.setVisible(False)
        self.btn_steps.setVisible(False)
        self.btn_prev_step.setVisible(False)
        self.btn_next_step.setVisible(False)
        self.btn_stop.setVisible(True)
        self.start_solution(is_steps=True)

    def btn_prev_step_clicked(self):
        if self.solution_current_step == 0:
            return QMessageBox.information(self, 'Cannot perform operation.', 'No information available')
        else:
            self.solution_current_step -= 1
            self.update_solution_table()

    def btn_next_step_clicked(self):
        if not self.is_running:
            return QMessageBox.information(self, 'Cannot perform operation.', 'Not running')
        elif self.solution_current_step < len(self.solution_steps) - 1:
            self.solution_current_step += 1
            self.update_solution_table()
        else:
            self.resume_solution(1)

    def btn_stop_clicked(self):
        self.stop_solution()

    def start_solution(self, is_steps=False):
        self.solution_event.clear()
        self.solution_steps = []
        self.solution_current_step = 0
        self.solution_thread = self.solution_class(name=self.name,
                                                   is_steps=is_steps,
                                                   pause_signal=self.solution_pause_signal,
                                                   resume_signal=self.solution_resume_signal,
                                                   return_signal=self.solution_return_signal,
                                                   stop_signal=self.solution_stop_signal,
                                                   event=self.solution_event)
        for param in self.params:
            setattr(self.solution_thread,
                    param['var_name'],
                    parser.parse_param(param['type'], param['qt_input'].toPlainText()))
        self.solution_thread.start()

    def pause_solution(self):
        self.is_steps = True
        self.solution_pause_signal.emit()

    def resume_solution(self, steps_num=0):  # 0 means no_wait
        self.is_steps = bool(steps_num)
        self.solution_resume_signal.emit(steps_num)
        self.solution_event.set()

    def stop_solution(self):
        self.btn_solve.setVisible(False)
        self.btn_pause_resume.setVisible(False)
        self.btn_pause_resume.setText('Pause')
        self.btn_steps.setVisible(False)
        self.btn_prev_step.setVisible(False)
        self.btn_next_step.setVisible(False)
        self.btn_stop.setVisible(False)
        self.solution_stop_signal.emit()
        self.solution_thread.wait()
        self.solution_thread.exiting = True
        self.solution_thread = None
        logging.warning('thread destroyed')
        #self.solution_return_signal.disconnect()
        #self.solution_resume_signal.disconnect()
        #self.solution_pause_signal.disconnect()
        self.solution_stop_signal.disconnect()
        self.solution_thread = None
        self.btn_solve.setVisible(True)
        self.btn_steps.setVisible(True)

    def proceed_solution(self, sln):
        if not sln:
            logging.warning('solution end')
            return self.stop_solution()
        elif 'error' in sln:
            #logging.warning('solution end by error %s' % sln['error'])
            return
        logging.warning('got solution %s' % sln)
        if self.is_steps:
            self.is_paused = True
            self.btn_pause_resume.setText('Resume')
            self.btn_pause_resume.setVisible(True)
            self.btn_prev_step.setVisible(True)
            self.btn_next_step.setVisible(True)
        else:
            self.solution_event.set()
        self.add_step_data(sln)
        self.solution_table.setVisible(True)

    def add_step_data(self, data):
        self.solution_steps.append(data)
        while len(self.solution_steps) > constants.queue_steps_max_size:
            self.solution_steps.pop(0)
        self.solution_current_step = len(self.solution_steps) - 1
        self.update_solution_table()

    def update_solution_table(self):
        self.solution_table.update_data(self.solution_steps[self.solution_current_step])

    @property
    def is_running(self):
        return bool(self.solution_thread) and self.solution_thread.isRunning()


class SolutionThread(QThread):
    def __init__(self, name, is_steps, pause_signal, resume_signal, return_signal, stop_signal, event):
        super(SolutionThread, self).__init__()
        self.name = name
        self.is_steps = is_steps
        pause_signal.connect(self.pause)
        resume_signal.connect(self.resume)
        self.return_signal = return_signal
        stop_signal.connect(self.stop)
        self.event = event
        self.steps = 0
        self.steps_left = 0
        self.exiting = False

    def pause(self):
        self.is_steps = True

    def resume(self, steps):
        self.is_steps = bool(steps)

    def run(self):
        self.return_signal.emit(dict())

    def start(self, thread_priority=QThread.InheritPriority):
        self.steps = 0
        super(SolutionThread, self).start(thread_priority)

    def return_step_solution(self, kwargs, final=False):
        if not final:
            self.steps += 1
        if self.steps_left:
            self.steps_left -= 1
        elif self.is_steps or final:
            kwargs['steps'] = self.steps
            self.return_signal.emit(kwargs)
            while not self.event.is_set() and not self.exiting:
                self.event.wait(timeout=0.05)
            self.event.clear()

    def return_final_solution(self, kwargs):
        if not self.is_steps:
            self.return_step_solution(kwargs, final=True)
        self.return_signal.emit(dict())

    def return_error_solution(self, error='stop'):
        if hasattr(self, 'error'):
            return
        self.error = True
        self.return_signal.emit({'error': error})

    def stop(self):
        if self.exiting:
            logging.critical('memory leak')
            #for i,x in enumerate(objgraph.by_type('CubicInterpolationSolution')):
            #    objgraph.show_chain(objgraph.find_backref_chain(x,objgraph.is_proper_module),filename='/home/oleg/memory-debug/%s_chain_%s.png'%(self,i))
            return
        logging.warning('exiting...')
        self.exiting = True


class SolutionTable(QTableView):
    def __init__(self):
        super(SolutionTable, self).__init__()
        self.setModel(SolutionTableModel(self))

    def update_data(self, data):
        self.model().set_data(data)


class SolutionTableModel(QAbstractTableModel):
    def __init__(self, parent, *args):
        super(SolutionTableModel, self).__init__(parent, *args)
        self.parent = parent
        self.data = [[]]
        self.header = []

    def rowCount(self, parent):
        return len(self.data)

    def columnCount(self, parent):
        return len(self.data[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.data[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def set_data(self, data):
        if py2:
            self.emit(SIGNAL("layoutAboutToBeChanged()"))
        else:
            self.layoutAboutToBeChanged.emit()
        self.header = list(data.keys())
        self.data = [[data[x] for x in self.header]]
        if py2:
            self.emit(SIGNAL("layoutChanged()"))
        else:
            self.layoutChanged.emit()
