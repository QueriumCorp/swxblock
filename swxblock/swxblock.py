"""This Xblock manages problems for Step-Wise Virtual Tutor(tm) from Querium Corp."""

import pkg_resources
import random

from xblock.core import XBlock
from xblock.fields import Integer, String, Scope, Dict, Float, Boolean
from web_fragments.fragment import Fragment
# McDaniel apr-2019: this is deprecated.
#from xblock.fragment import Fragment
from xblock.scorable import ScorableXBlockMixin, Score
from xblockutils.studio_editable import StudioEditableXBlockMixin
from lms.djangoapps.courseware.courses import get_course_by_id
from logging import getLogger
logger = getLogger(__name__)

"""
The general idea is that we'll determine which question parameters to pass to the StepWise client before invoking it,
making use of course-wide StepWise defaults if set.
If the student has exceeded the max mumber of attempts (course-wide setting or per-question setting), we won't let them
start another attempt.
We'll then get two call-backs:
1. When the student begins work on the question (e.g. submits a first step, clicks 'Hint', or clicks 'Show Solution'.
This will increment the attempts counter.
2. When the student completes the problem ('victory'), we'll store their grade on this attempt.
Note that the student can start an attempt, but never finish (abandoned attempt), but we will still want to count the attempt.
"""

@XBlock.wants('user')
@XBlock.needs('course')
class SWXBlock(StudioEditableXBlockMixin, XBlock):
    """
    This xblock provides up to 10 variants of a question for delivery using the StepWise UI.
    """
    logger.debug('SWXBlock() - instantiated')
    has_author_view = True # tells the xblock to not ignore the AuthorView
    has_score = True       # tells the xblock to not ignore the grade event
    show_in_read_only_mode = True # tells the xblock to let the instructor view the student's work (lms/djangoapps/courseware/masquerade.py)

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # Place to store the UUID for this xblock instance.  Not currently displayed in any view.
    url_name = String(display_name="URL name", default='NONE', scope=Scope.content)

    # PER-QUESTION GRADING OPTIONS (STILL NEED TO ALLOW FOR COURSE DEFAULTS)
    q_weight = Float(
        display_name="Problem Weight",
        help="Defines the number of points the problem is worth.",
        scope=Scope.content,
        default=1.0,
        enforce_type=True
    )

    q_grade_showme_ded = Float(help="Point deduction for using Show Solution", default=-1.0, scope=Scope.content)
    q_grade_hints_count = Integer(help="Number of Hints before deduction", default=-1, scope=Scope.content)
    q_grade_hints_ded = Float(help="Point deduction for using excessive Hints", default=-1.0, scope=Scope.content)
    q_grade_errors_count = Integer(help="Number of Errors before deduction", default=-1, scope=Scope.content)
    q_grade_errors_ded = Float(help="Point deduction for excessive Errors", default=-1.0, scope=Scope.content)
    q_grade_min_steps_count = Integer(help="Minimum valid steps in solution for full credit", default=3, scope=Scope.content)
    q_grade_min_steps_ded = Float(help="Point deduction for fewer than minimum valid steps", default=0.0, scope=Scope.content)

    # PER-QUESTION HINTS/SHOW SOLUTION OPTIONS
    q_option_hint = Boolean(help='Display Hint button if "True"', default=True, scope=Scope.content)
    q_option_showme = Boolean(help='Display ShowSolution button if "True"', default=True, scope=Scope.content)

    # MAX ATTEMPTS PER-QUESTION OVERRIDE OF COURSE DEFAULT
    q_max_attempts = Integer(help="Max question attempts (-1 = Use Course Default)", default=-1, scope=Scope.content)

    # STEP-WISE QUESTION DEFINITION FIELDS FOR TEN VARIANTS
    display_name = String(display_name="Display name", default='StepWise', scope=Scope.content)

    q_id = String(help="Question ID", default="", scope=Scope.content)
    q_label = String(help="Question label", default="", scope=Scope.content)
    q_stimulus = String(help="Stimulus", default='Solve for \\(a\\).', scope=Scope.content)
    q_definition = String(help="Definition", default='SolveFor[5a+4=2a-5,a]', scope=Scope.content)
    q_type = String(help="Type", default='gradeBasicAlgebra', scope=Scope.content)
    q_display_math = String(help="Display Math", default='\\(\\)', scope=Scope.content)
    q_hint1 = String(help="First Hint", default='', scope=Scope.content)
    q_hint2 = String(help="Second Hint", default='', scope=Scope.content)
    q_hint3 = String(help="Third Hint", default='', scope=Scope.content)

    q1_id = String(help="Question ID", default="", scope=Scope.content)
    q1_label = String(help="Question Alternate 1", default="", scope=Scope.content)
    q1_stimulus = String(help="Stimulus", default='', scope=Scope.content)
    q1_definition = String(help="Definition", default='', scope=Scope.content)
    q1_type = String(help="Type", default='gradeBasicAlgebra', scope=Scope.content)
    q1_display_math = String(help="Display Math", default='\\(\\)', scope=Scope.content)
    q_grade_hints_ded = Integer(help="Deduction for using extra Hints", default=-1, scope=Scope.content)
    q1_hint1 = String(help="First Hint", default='', scope=Scope.content)
    q1_hint2 = String(help="Second Hint", default='', scope=Scope.content)
    q1_hint3 = String(help="Third Hint", default='', scope=Scope.content)

    q2_id = String(help="Question ID", default="", scope=Scope.content)
    q2_label = String(help="Question Alternate 2", default="", scope=Scope.content)
    q2_stimulus = String(help="Stimulus", default='', scope=Scope.content)
    q2_definition = String(help="Definition", default='', scope=Scope.content)
    q2_type = String(help="Type", default='gradeBasicAlgebra', scope=Scope.content)
    q2_display_math = String(help="Display Math", default='\\(\\)', scope=Scope.content)
    q2_hint1 = String(help="First Hint", default='', scope=Scope.content)
    q2_hint2 = String(help="Second Hint", default='', scope=Scope.content)
    q2_hint3 = String(help="Third Hint", default='', scope=Scope.content)

    q3_id = String(help="Question ID", default="", scope=Scope.content)
    q3_label = String(help="Question Alternate 3", default="", scope=Scope.content)
    q3_stimulus = String(help="Stimulus", default='', scope=Scope.content)
    q3_definition = String(help="Definition", default='', scope=Scope.content)
    q3_type = String(help="Type", default='gradeBasicAlgebra', scope=Scope.content)
    q3_display_math = String(help="Display Math", default='\\(\\)', scope=Scope.content)
    q3_hint1 = String(help="First Hint", default='', scope=Scope.content)
    q3_hint2 = String(help="Second Hint", default='', scope=Scope.content)
    q3_hint3 = String(help="Third Hint", default='', scope=Scope.content)

    q4_id = String(help="Question ID", default="", scope=Scope.content)
    q4_label = String(help="Question Alternate 4", default="", scope=Scope.content)
    q4_stimulus = String(help="Stimulus", default='', scope=Scope.content)
    q4_definition = String(help="Definition", default='', scope=Scope.content)
    q4_type = String(help="Type", default='gradeBasicAlgebra', scope=Scope.content)
    q4_display_math = String(help="Display Math", default='\\(\\)', scope=Scope.content)
    q4_hint1 = String(help="First Hint", default='', scope=Scope.content)
    q4_hint2 = String(help="Second Hint", default='', scope=Scope.content)
    q4_hint3 = String(help="Third Hint", default='', scope=Scope.content)

    q5_id = String(help="Question ID", default="", scope=Scope.content)
    q5_label = String(help="Question Alternate 5", default="", scope=Scope.content)
    q5_stimulus = String(help="Stimulus", default='', scope=Scope.content)
    q5_definition = String(help="Definition", default='', scope=Scope.content)
    q5_type = String(help="Type", default='gradeBasicAlgebra', scope=Scope.content)
    q5_display_math = String(help="Display Math", default='\\(\\)', scope=Scope.content)
    q5_hint1 = String(help="First Hint", default='', scope=Scope.content)
    q5_hint2 = String(help="Second Hint", default='', scope=Scope.content)
    q5_hint3 = String(help="Third Hint", default='', scope=Scope.content)

    q6_id = String(help="Question ID", default="", scope=Scope.content)
    q6_label = String(help="Question Alternate 6", default="", scope=Scope.content)
    q6_stimulus = String(help="Stimulus", default='', scope=Scope.content)
    q6_definition = String(help="Definition", default='', scope=Scope.content)
    q6_type = String(help="Type", default='gradeBasicAlgebra', scope=Scope.content)
    q6_display_math = String(help="Display Math", default='\\(\\)', scope=Scope.content)
    q6_hint1 = String(help="First Hint", default='', scope=Scope.content)
    q6_hint2 = String(help="Second Hint", default='', scope=Scope.content)
    q6_hint3 = String(help="Third Hint", default='', scope=Scope.content)

    q7_id = String(help="Question ID", default="", scope=Scope.content)
    q7_label = String(help="Question Alternate 7", default="", scope=Scope.content)
    q7_stimulus = String(help="Stimulus", default='', scope=Scope.content)
    q7_definition = String(help="Definition", default='', scope=Scope.content)
    q7_type = String(help="Type", default='gradeBasicAlgebra', scope=Scope.content)
    q7_display_math = String(help="Display Math", default='\\(\\)', scope=Scope.content)
    q7_hint1 = String(help="First Hint", default='', scope=Scope.content)
    q7_hint2 = String(help="Second Hint", default='', scope=Scope.content)
    q7_hint3 = String(help="Third Hint", default='', scope=Scope.content)

    q8_id = String(help="Question ID", default="", scope=Scope.content)
    q8_label = String(help="Question Alternate 8", default="", scope=Scope.content)
    q8_stimulus = String(help="Stimulus", default='', scope=Scope.content)
    q8_definition = String(help="Definition", default='', scope=Scope.content)
    q8_type = String(help="Type", default='gradeBasicAlgebra', scope=Scope.content)
    q8_display_math = String(help="Display Math", default='\\(\\)', scope=Scope.content)
    q8_hint1 = String(help="First Hint", default='', scope=Scope.content)
    q8_hint2 = String(help="Second Hint", default='', scope=Scope.content)
    q8_hint3 = String(help="Third Hint", default='', scope=Scope.content)

    q9_id = String(help="Question ID", default="", scope=Scope.content)
    q9_label = String(help="Question Alternate 9", default="", scope=Scope.content)
    q9_stimulus = String(help="Stimulus", default='', scope=Scope.content)
    q9_definition = String(help="Definition", default='', scope=Scope.content)
    q9_type = String(help="Type", default='gradeBasicAlgebra', scope=Scope.content)
    q9_display_math = String(help="Display Math", default='\\(\\)', scope=Scope.content)
    q9_hint1 = String(help="First Hint", default='', scope=Scope.content)
    q9_hint2 = String(help="Second Hint", default='', scope=Scope.content)
    q9_hint3 = String(help="Third Hint", default='', scope=Scope.content)

    # STUDENT'S QUESTION PERFORMANCE FIELDS
    grade = Float(help="The student's grade", default=-1, scope=Scope.user_state)
    solution = Dict(help="The student's last solution", default={}, scope=Scope.user_state)
    # count_attempts keeps track of the number of attempts of this question by this student so we can
    # compare to course.max_attempts which is inherited as an per-question setting or a course-wide setting.
    count_attempts = Integer(help="Counted number of questions attempts", default=0, scope=Scope.user_state)

    raw_possible = Float(help="Number of possible points", default=3,scope=Scope.user_state)

    # FIELDS FOR THE ScorableXBlockMixin

    is_answered = Boolean(
        default=False,
        scope=Scope.user_state,
        help='Will be set to "True" if successfully answered'
    )

    correct = Boolean(
        default=False,
        scope=Scope.user_state,
        help='Will be set to "True" if correctly answered'
    )

    raw_earned = Float(
        help="Keeps maximum score achieved by student as a raw value between 0 and 1.",
        scope=Scope.user_state,
        default=0,
        enforce_type=True,
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # STUDENT_VIEW
    def student_view(self, context=None):
        """
        The STUDENT view of the SWXBlock, shown to students
        when viewing courses.  We set up the question parameters (referring to course-wide settings), then launch
        the javascript StepWise client.
        """
        logger.info('SWXblock student_view() - entered')
        logger.info("SWXblock student_view() self={a}".format(a=self))
        logger.info("SWXblock student_view() self.runtime={a}".format(a=self.runtime))
        logger.info("SWXblock student_view() self.runtime.course_id={a}".format(a=self.runtime.course_id))

        course = get_course_by_id(self.runtime.course_id)
        logger.info("SWXblock student_view() course={c}".format(c=course))

        logger.info("SWXblock student_view() max_attempts={a} q_max_attempts={b}".format(a=self.max_attempts,b=self.q_max_attempts))

	# NOTE: Can't set a self.q_* field here if an older imported swxblock doesn't define this field, since it defaults to None
        # (read only?) so we'll use a local var my_* to remember whether to use the course-wide setting or the per-question setting.
	# Similarly, some old courses may not define the stepwise advanced settings we want, so we create local variables for them.

        # For per-xblock settings
        temp_max_attempts = -1
        temp_option_hint = -1
        temp_option_showme = -1
        temp_grade_hints_count = -1
        temp_grade_hints_ded = -1
        temp_grade_errors_count = -1
        temp_grade_errors_ded = -1
        temp_grade_min_steps_count = -1
        temp_grade_min_steps_ded = -1

        # For course-wide settings
        temp_settings_stepwise_max_attempts = -1
        temp_settings_stepwise_option_hint = -1
        temp_settings_stepwise_option_showme = -1
        temp_settings_stepwise_grade_hints_count = -1
        temp_settings_stepwise_grade_hints_ded = -1
        temp_settings_stepwise_grade_errors_count = -1
        temp_settings_stepwise_grade_errors_ded = -1
        temp_settings_stepwise_grade_min_steps_count = -1
        temp_settings_stepwise_grade_min_steps_ded = -1

        # after application of course-wide settings
	my_max_attempts = -1
	my_option_showme = -1
	my_option_hint = -1
	my_grade_hints_count = -1
	my_grade_hints_ded = -1
	my_grade_errors_count = -1
	my_grade_errors_ded = -1
	my_grade_min_steps_count = -1
	my_grade_min_steps_ded = -1

        # Fetch the xblock-specific settings if they exist, otherwise create a default
        try:
            temp_max_attempts = self.q_max_attempts
        except (NameError,AttributeError) as e:
            logger.info('SWXblock student_view() - self.q_max_attempts was not defined in this instance: {e}'.format(e=e))
            temp_max_attempts = -1
        logger.info('SWXblock student_view() - temp_max_attempts: {t}'.format(t=temp_max_attempts))

        try:
            temp_option_hint = self.q_option_hint
        except (NameError,AttributeError) as e:
            logger.info('SWXblock student_view() - self.option_hint was not defined in this instance: {e}'.format(e=e))
            temp_option_hint = -1
        logger.info('SWXblock student_view() - temp_option_hint: {t}'.format(t=temp_option_hint))

        try:
            temp_option_showme = self.q_option_showme
        except (NameError,AttributeError) as e:
            logger.info('SWXblock student_view() - self.option_showme was not defined in this instance: {e}'.format(e=e))
            temp_option_showme = -1
        logger.info('SWXblock student_view() - temp_option_showme: {t}'.format(t=temp_option_showme))

        try:
            temp_grade_hints_count = self.q_grade_hints_count
        except (NameError,AttributeError) as e:
            logger.info('SWXblock student_view() - self.q_grade_hints_count was not defined in this instance: {e}'.format(e=e))
            temp_grade_hints_count = -1
        logger.info('SWXblock student_view() - temp_grade_hints_count: {t}'.format(t=temp_grade_hints_count))

        try:
            temp_grade_hints_ded = self.q_grade_hints_ded
        except (NameError,AttributeError) as e:
            logger.info('SWXblock student_view() - self.q_grade_hints_ded was not defined in this instance: {e}'.format(e=e))
            temp_grade_hints_ded = -1
        logger.info('SWXblock student_view() - temp_grade_hints_ded: {t}'.format(t=temp_grade_hints_ded))

        try:
            temp_grade_errors_count = self.q_grade_errors_count
        except (NameError,AttributeError) as e:
            logger.info('SWXblock student_view() - self.q_grade_errors_count was not defined in this instance: {e}'.format(e=e))
            temp_grade_errors_count = -1
        logger.info('SWXblock student_view() - temp_grade_errors_count: {t}'.format(t=temp_grade_errors_count))

        try:
            temp_grade_errors_ded = self.q_grade_errors_ded
        except (NameError,AttributeError) as e:
            logger.info('SWXblock student_view() - self.q_grade_errors_ded was not defined in this instance: {e}'.format(e=e))
            temp_grade_errors_ded = -1
        logger.info('SWXblock student_view() - temp_grade_errors_ded: {t}'.format(t=temp_grade_errors_ded))

        try:
            temp_grade_min_steps_count = self.q_grade_min_steps_count
        except (NameError,AttributeError) as e:
            logger.info('SWXblock student_view() - self.q_grade_min_steps_count was not defined in this instance: {e}'.format(e=e))
            temp_grade_min_steps_count = -1
        logger.info('SWXblock student_view() - temp_grade_min_steps_count: {t}'.format(t=temp_grade_min_steps_count))

        try:
            temp_grade_min_steps_ded = self.q_grade_min_steps_ded
        except (NameError,AttributeError) as e:
            logger.info('SWXblock student_view() - self.q_grade_min_steps_ded was not defined in this instance: {e}'.format(e=e))
            temp_grade_min_steps_ded = -1
        logger.info('SWXblock student_view() - temp_grade_min_steps_ded: {t}'.format(t=temp_grade_min_steps_ded))

        # Fetch the course-wide settings if they exist, otherwise create a default

        try:
            temp_settings_stepwise_max_attempts = course.settings.stepwise_max_attempts
        except (NameError,AttributeError) as e:
            logger.info('SWXblock student_view() - course.settings.stepwise_max_attempts was not defined in this instance: {e}'.format(e=e))
            temp_stepwise_stepwise_max_attempts = -1
        logger.info('SWXblock student_view() - temp_stepwise_max_attempts: {s}'.format(s=temp_settings_stepwise_max_attempts))

        try:
            temp_settings_stepwise_option_showme = course.settings.stepwise_option_showme
        except (NameError,AttributeError) as e:
            logger.info('SWXblock student_view() - course.settings.stepwise_option_showme was not defined in this instance: {e}'.format(e=e))
            temp_settings_stepwise_option_showme = -1
        logger.info('SWXblock student_view() - temp_stepwise_option_showme: {s}'.format(s=temp_settings_stepwise_option_showme))

        try:
            temp_settings_stepwise_option_hint = course.settings.stepwise_option_hint
        except (NameError,AttributeError) as e:
            logger.info('SWXblock student_view() - course.settings.stepwise_option_hint was not defined in this instance: {e}'.format(e=e))
            temp_settings_stepwise_option_hint = -1
        logger.info('SWXblock student_view() - temp_settings_stepwise_option_hint: {s}'.format(s=temp_settings_stepwise_option_hint))

        try:
            temp_settings_stepwise_hints_count = course.settings.stepwise_hints_count
        except (NameError,AttributeError) as e:
            logger.info('SWXblock student_view() - course.settings.stepwise_hints_count was not defined in this instance: {e}'.format(e=e))
            temp_settings_stepwise_hints_count = -1
        logger.info('SWXblock student_view() - temp_settings_stepwise_hints_count: {s}'.format(s=temp_settings_stepwise_hints_count))

        try:
            temp_settings_stepwise_hints_ded = course.settings.stepwise_hints_ded
        except (NameError,AttributeError) as e:
            logger.info('SWXblock student_view() - course.settings.stepwise_hints_ded was not defined in this instance: {e}'.format(e=e))
            temp_settings_stepwise_hints_ded = -1
        logger.info('SWXblock student_view() - temp_settings_stepwise_hints_ded: {s}'.format(s=temp_settings_stepwise_hints_ded))

        try:
            temp_settings_stepwise_errors_count = course.settings.stepwise_errors_count
        except (NameError,AttributeError) as e:
            logger.info('SWXblock student_view() - course.settings.stepwise_errors_count was not defined in this instance: {e}'.format(e=e))
            temp_settings_stepwise_errors_count = -1
        logger.info('SWXblock student_view() - temp_settings_stepwise_errors_count: {s}'.format(s=temp_settings_stepwise_errors_count))

        try:
            temp_settings_stepwise_errors_ded = course.settings.stepwise_errors_ded
        except (NameError,AttributeError) as e:
            logger.info('SWXblock student_view() - course.settings.stepwise_errors_ded was not defined in this instance: {e}'.format(e=e))
            temp_settings_stepwise_errors_ded = -1
        logger.info('SWXblock student_view() - temp_settings_stepwise_errors_ded: {s}'.format(s=temp_settings_stepwise_errors_ded))

        try:
            temp_settings_stepwise_min_steps_count = course.settings.stepwise_min_steps_count
        except (NameError,AttributeError) as e:
            logger.info('SWXblock student_view() - course.settings.stepwise_min_steps_count was not defined in this instance: {e}'.format(e=e))
            temp_settings_stepwise_min_steps_count = -1
        logger.info('SWXblock student_view() - temp_settings_stepwise_min_steps_count: {s}'.format(s=temp_settings_stepwise_min_steps_count))

        try:
            temp_settings_stepwise_min_steps_ded = course.settings.stepwise_min_steps_ded
        except (NameError,AttributeError) as e:
            logger.info('SWXblock student_view() - course.settings.stepwise_min_steps_ded was not defined in this instance: {e}'.format(e=e))
            temp_settings_stepwise_min_steps_ded = -1
        logger.info('SWXblock student_view() - temp_settings_stepwise_min_steps_ded: {s}'.format(s=temp_settings_stepwise_min_steps_ded))

        # Enforce course-wide grading options here.
	# We prefer the per-question setting to the course setting.

        # For max_attempts: If there is a per-question max_attempts setting, use that.
        # Otherwise, if there is a course-wide stepwise_max_attempts setting, use that.
        # Otherwise, use the course-wide max_attempts setting that is used for CAPA (non-StepWise) problems.
        if (temp_grade_max_attempts != -1):
            my_grade_max_attempts = temp_grade_max_attempts
        elif (temp_settings_stepwise_max_attempts != -1):
            my_grade_max_attempts = temp_settings_stepwise_max_attempts
        else:
            my_grade_max_attempts = course.settings.stepwise_max_attempts
        logger.info('SWXblock student_view() - my_max_attempts={m}'.format(m=my_max_attempts))

        if (temp_option_hint != -1):
            my_option_hint = temp_option_hint
        elif (temp_settings_stepwise_option_hint != -1):
            my_option_hint = temp_settings_stepwise_option_hint
        logger.info('SWXblock student_view() - my_option_hint={m}'.format(m=my_option_hint))

        if (temp_option_showme != -1):
            my_option_showme = temp_option_showme
        elif (temp_settings_stepwise_option_showme != -1):
            my_option_showme = temp_settings_stepwise_option_showme
        logger.info('SWXblock student_view() - my_option_showme={m}'.format(m=my_option_showme))

        if (temp_grade_hints_count != -1):
            my_grade_hints_count = temp_grade_hints_count
        elif (temp_settings_stepwise_hints_count != -1):
            my_grade_hints_count = temp_settings_stepwise_hints_count
        logger.info('SWXblock student_view() - my_grade_hints_count={m}'.format(m=my_grade_hints_count))

        if (temp_grade_hints_ded != -1):
            my_grade_hints_ded = temp_grade_hints_ded
        elif (temp_settings_stepwise_hints_ded != -1):
            my_grade_hints_ded = temp_settings_stepwise_hints_ded
        logger.info('SWXblock student_view() - my_grade_hints_ded={m}'.format(m=my_grade_hints_ded))

        if (temp_grade_errors_count != -1):
            my_grade_errors_count = temp_grade_errors_count
        elif (temp_settings_stepwise_errors_count != -1):
            my_grade_errors_count = temp_settings_stepwise_errors_count
        logger.info('SWXblock student_view() - my_grade_errors_count={m}'.format(m=my_grade_errors_count))

        if (temp_grade_errors_ded != -1):
            my_grade_errors_ded = temp_grade_errors_ded
        elif (temp_settings_stepwise_errors_ded != -1):
            my_grade_errors_ded = temp_settings_stepwise_errors_ded
        logger.info('SWXblock student_view() - my_grade_errors_ded={m}'.format(m=my_grade_errors_ded))

        if (temp_grade_min_steps_count != -1):
            my_grade_min_steps_count = temp_grade_min_steps_count
        elif (temp_settings_stepwise_min_steps_count != -1):
            my_grade_min_steps_count = temp_settings_stepwise_min_steps_count
        logger.info('SWXblock student_view() - my_grade_min_steps_count={m}'.format(m=my_grade_min_steps_count))

        if (temp_grade_min_steps_ded != -1):
            my_grade_min_steps_ded = temp_grade_min_steps_ded
        elif (temp_settings_stepwise_min_steps_ded != -1):
            my_grade_min_steps_ded = temp_settings_stepwise_min_steps_ded
        logger.info('SWXblock student_view() - my_grade_min_steps_ded={m}'.format(m=my_grade_min_steps_ded))


        # Save an identifier for the user

        user_service = self.runtime.service( self, 'user')
        xb_user = user_service.get_current_user()

        # Determine which stepwise variant to use

        if len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0 and len(self.q3_definition)>0 and len(self.q4_definition)>0 and len(self.q5_definition)>0 and len(self.q6_definition)>0 and len(self.q7_definition)>0 and len(self.q8_definition)>0  and len(self.q9_definition)>0:
            q_index = random.randint(0, 999)
        elif len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0 and len(self.q3_definition)>0 and len(self.q4_definition)>0 and len(self.q5_definition)>0 and len(self.q6_definition)>0 and len(self.q7_definition)>0 and len(self.q8_definition)>0:
            q_index = random.randint(0, 899)
        elif len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0 and len(self.q3_definition)>0 and len(self.q4_definition)>0 and len(self.q5_definition)>0 and len(self.q6_definition)>0 and len(self.q7_definition)>0:
            q_index = random.randint(0, 799)
        elif len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0 and len(self.q3_definition)>0 and len(self.q4_definition)>0 and len(self.q5_definition)>0 and len(self.q6_definition)>0:
            q_index = random.randint(0, 699)
        elif len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0 and len(self.q3_definition)>0 and len(self.q4_definition)>0 and len(self.q5_definition)>0:
            q_index = random.randint(0, 599)
        elif len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0 and len(self.q3_definition)>0 and len(self.q4_definition)>0:
            q_index = random.randint(0, 499)
        elif len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0 and len(self.q3_definition)>0:
            q_index = random.randint(0, 399)
        elif len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0:
            q_index = random.randint(0, 299)
        elif len(self.q_definition)>0 and len(self.q1_definition)>0:
            q_index = random.randint(0, 199)
        else:
            q_index = 0

        if q_index>=0 and q_index<100:
            question = {
                "q_id" : self.q_id,
                "q_user" : xb_user.emails[0],
                "q_index" : 0,
                "q_label" : self.q_label,
                "q_stimulus" : self.q_stimulus,
                "q_definition" : self.q_definition,
                "q_type" :  self.q_type,
                "q_display_math" :  self.q_display_math,
                "q_hint1" :  self.q_hint1,
                "q_hint2" :  self.q_hint2,
                "q_hint3" :  self.q_hint3,
                "q_weight" :  self.q_weight,
                "q_max_attempts" : my_max_attempts,
                "q_option_hint" : my_option_hint,
                "q_option_showme" : my_option_showme,
                "q_grade_showme_ded" : my_grade_showme_ded,
                "q_grade_hints_count" : my_grade_hints_count,
                "q_grade_hints_ded" : my_grade_hints_ded,
                "q_grade_errors_count" : my_grade_errors_count,
                "q_grade_errors_ded" : my_grade_errors_ded,
		"q_grade_min_steps_count" : my_grade_min_steps_count,
		"q_grade_min_steps_ded" : my_grade_min_steps_ded
            }
        elif q_index>=100 and q_index<200:
            question = {
                "q_id" : self.q1_id,
                "q_user" : xb_user.emails[0],
                "q_index" : 1,
                "q_label" : self.q1_label,
                "q_stimulus" : self.q1_stimulus,
                "q_definition" : self.q1_definition,
                "q_type" :  self.q1_type,
                "q_display_math" :  self.q1_display_math,
                "q_hint1" :  self.q1_hint1,
                "q_hint2" :  self.q1_hint2,
                "q_hint3" :  self.q1_hint3,
                "q_weight" :  my_weight,
                "q_max_attempts" : my_max_attempts,
                "q_option_hint" : my_option_hint,
                "q_option_showme" : my_option_showme,
                "q_grade_showme_ded" : my_grade_showme_ded,
                "q_grade_hints_count" : my_grade_hints_count,
                "q_grade_hints_ded" : my_grade_hints_ded,
                "q_grade_errors_count" : my_grade_errors_count,
                "q_grade_errors_ded" : my_grade_errors_ded,
		"q_grade_min_steps_count" : my_grade_min_steps_count,
		"q_grade_min_steps_ded" : my_grade_min_steps_ded
            }
        elif q_index>=200 and q_index<300:
            question = {
                "q_id" : self.q2_id,
                "q_user" : xb_user.emails[0],
                "q_index" : 2,
                "q_label" : self.q2_label,
                "q_stimulus" : self.q2_stimulus,
                "q_definition" : self.q2_definition,
                "q_type" :  self.q2_type,
                "q_display_math" :  self.q2_display_math,
                "q_hint1" :  self.q2_hint1,
                "q_hint2" :  self.q2_hint2,
                "q_hint3" :  self.q2_hint3,
                "q_weight" :  my_weight,
                "q_max_attempts" : my_max_attempts,
                "q_option_hint" : my_option_hint,
                "q_option_showme" : my_option_showme,
                "q_grade_showme_ded" : my_grade_showme_ded,
                "q_grade_hints_count" : my_grade_hints_count,
                "q_grade_hints_ded" : my_grade_hints_ded,
                "q_grade_errors_count" : my_grade_errors_count,
                "q_grade_errors_ded" : my_grade_errors_ded,
		"q_grade_min_steps_count" : my_grade_min_steps_count,
		"q_grade_min_steps_ded" : my_grade_min_steps_ded
            }
        elif q_index>=300 and q_index<400:
            question = {
                "q_id" : self.q3_id,
                "q_user" : xb_user.emails[0],
                "q_index" : 3,
                "q_label" : self.q3_label,
                "q_stimulus" : self.q3_stimulus,
                "q_definition" : self.q3_definition,
                "q_type" :  self.q3_type,
                "q_display_math" :  self.q3_display_math,
                "q_hint1" :  self.q3_hint1,
                "q_hint2" :  self.q3_hint2,
                "q_hint3" :  self.q3_hint3,
                "q_weight" :  my_weight,
                "q_max_attempts" : my_max_attempts,
                "q_option_hint" : my_option_hint,
                "q_option_showme" : my_option_showme,
                "q_grade_showme_ded" : my_grade_showme_ded,
                "q_grade_hints_count" : my_grade_hints_count,
                "q_grade_hints_ded" : my_grade_hints_ded,
                "q_grade_errors_count" : my_grade_errors_count,
                "q_grade_errors_ded" : my_grade_errors_ded,
		"q_grade_min_steps_count" : my_grade_min_steps_count,
		"q_grade_min_steps_ded" : my_grade_min_steps_ded
            }
        elif q_index>=400 and q_index<500:
            question = {
                "q_id" : self.q4_id,
                "q_user" : xb_user.emails[0],
                "q_index" : 4,
                "q_label" : self.q4_label,
                "q_stimulus" : self.q4_stimulus,
                "q_definition" : self.q4_definition,
                "q_type" :  self.q4_type,
                "q_display_math" :  self.q4_display_math,
                "q_hint1" :  self.q4_hint1,
                "q_hint2" :  self.q4_hint2,
                "q_hint3" :  self.q4_hint3,
                "q_weight" :  my_weight,
                "q_max_attempts" : my_max_attempts,
                "q_option_hint" : my_option_hint,
                "q_option_showme" : my_option_showme,
                "q_grade_showme_ded" : my_grade_showme_ded,
                "q_grade_hints_count" : my_grade_hints_count,
                "q_grade_hints_ded" : my_grade_hints_ded,
                "q_grade_errors_count" : my_grade_errors_count,
                "q_grade_errors_ded" : my_grade_errors_ded,
		"q_grade_min_steps_count" : my_grade_min_steps_count,
		"q_grade_min_steps_ded" : my_grade_min_steps_ded
            }
        elif q_index>=500 and q_index<600:
            question = {
                "q_id" : self.q5_id,
                "q_user" : xb_user.emails[0],
                "q_index" : 5,
                "q_label" : self.q5_label,
                "q_stimulus" : self.q5_stimulus,
                "q_definition" : self.q5_definition,
                "q_type" :  self.q5_type,
                "q_display_math" :  self.q5_display_math,
                "q_hint1" :  self.q5_hint1,
                "q_hint2" :  self.q5_hint2,
                "q_hint3" :  self.q5_hint3,
                "q_weight" :  my_weight,
                "q_max_attempts" : my_max_attempts,
                "q_option_hint" : my_option_hint,
                "q_option_showme" : my_option_showme,
                "q_grade_showme_ded" : my_grade_showme_ded,
                "q_grade_hints_count" : my_grade_hints_count,
                "q_grade_hints_ded" : my_grade_hints_ded,
                "q_grade_errors_count" : my_grade_errors_count,
                "q_grade_errors_ded" : my_grade_errors_ded,
		"q_grade_min_steps_count" : my_grade_min_steps_count,
		"q_grade_min_steps_ded" : my_grade_min_steps_ded
            }
        elif q_index>=600 and q_index<700:
            question = {
                "q_id" : self.q6_id,
                "q_user" : xb_user.emails[0],
                "q_index" : 6,
                "q_label" : self.q6_label,
                "q_stimulus" : self.q6_stimulus,
                "q_definition" : self.q6_definition,
                "q_type" :  self.q6_type,
                "q_display_math" :  self.q6_display_math,
                "q_hint1" :  self.q6_hint1,
                "q_hint2" :  self.q6_hint2,
                "q_hint3" :  self.q6_hint3,
                "q_weight" :  my_weight,
                "q_max_attempts" : my_max_attempts,
                "q_option_hint" : my_option_hint,
                "q_option_showme" : my_option_showme,
                "q_grade_showme_ded" : my_grade_showme_ded,
                "q_grade_hints_count" : my_grade_hints_count,
                "q_grade_hints_ded" : my_grade_hints_ded,
                "q_grade_errors_count" : my_grade_errors_count,
                "q_grade_errors_ded" : my_grade_errors_ded,
		"q_grade_min_steps_count" : my_grade_min_steps_count,
		"q_grade_min_steps_ded" : my_grade_min_steps_ded
            }
        elif q_index>=700 and q_index<800:
            question = {
                "q_id" : self.q7_id,
                "q_user" : xb_user.emails[0],
                "q_index" : 7,
                "q_label" : self.q7_label,
                "q_stimulus" : self.q7_stimulus,
                "q_definition" : self.q7_definition,
                "q_type" :  self.q7_type,
                "q_display_math" :  self.q7_display_math,
                "q_hint1" :  self.q7_hint1,
                "q_hint2" :  self.q7_hint2,
                "q_hint3" :  self.q7_hint3,
                "q_weight" :  my_weight,
                "q_max_attempts" : my_max_attempts,
                "q_option_hint" : my_option_hint,
                "q_option_showme" : my_option_showme,
                "q_grade_showme_ded" : my_grade_showme_ded,
                "q_grade_hints_count" : my_grade_hints_count,
                "q_grade_hints_ded" : my_grade_hints_ded,
                "q_grade_errors_count" : my_grade_errors_count,
                "q_grade_errors_ded" : my_grade_errors_ded,
		"q_grade_min_steps_count" : my_grade_min_steps_count,
		"q_grade_min_steps_ded" : my_grade_min_steps_ded
            }
        elif q_index>=800 and q_index<900:
            question = {
                "q_id" : self.q8_id,
                "q_user" : xb_user.emails[0],
                "q_index" : 8,
                "q_label" : self.q8_label,
                "q_stimulus" : self.q8_stimulus,
                "q_definition" : self.q8_definition,
                "q_type" :  self.q8_type,
                "q_display_math" :  self.q8_display_math,
                "q_hint1" :  self.q8_hint1,
                "q_hint2" :  self.q8_hint2,
                "q_hint3" :  self.q8_hint3,
                "q_weight" :  my_weight,
                "q_max_attempts" : my_max_attempts,
                "q_option_hint" : my_option_hint,
                "q_option_showme" : my_option_showme,
                "q_grade_showme_ded" : my_grade_showme_ded,
                "q_grade_hints_count" : my_grade_hints_count,
                "q_grade_hints_ded" : my_grade_hints_ded,
                "q_grade_errors_count" : my_grade_errors_count,
                "q_grade_errors_ded" : my_grade_errors_ded,
		"q_grade_min_steps_count" : my_grade_min_steps_count,
		"q_grade_min_steps_ded" : my_grade_min_steps_ded
            }
        else:
            question = {
                "q_id" : self.q9_id,
                "q_user" : xb_user.emails[0],
                "q_index" : 9,
                "q_label" : self.q9_label,
                "q_stimulus" : self.q9_stimulus,
                "q_definition" : self.q9_definition,
                "q_type" :  self.q9_type,
                "q_display_math" :  self.q9_display_math,
                "q_hint1" :  self.q9_hint1,
                "q_hint2" :  self.q9_hint2,
                "q_hint3" :  self.q9_hint3,
                "q_weight" :  my_weight,
                "q_max_attempts" : my_max_attempts,
                "q_option_hint" : my_option_hint,
                "q_option_showme" : my_option_showme,
                "q_grade_showme_ded" : my_grade_showme_ded,
                "q_grade_hints_count" : my_grade_hints_count,
                "q_grade_hints_ded" : my_grade_hints_ded,
                "q_grade_errors_count" : my_grade_errors_count,
                "q_grade_errors_ded" : my_grade_errors_ded,
		"q_grade_min_steps_count" : my_grade_min_steps_count,
		"q_grade_min_steps_ded" : my_grade_min_steps_ded
            }

        data = {
            "question" : question,
            "grade" :self.grade,
            "solution" : self.solution,
            "count_attempts" : self.count_attempts
        }

        html = self.resource_string("static/html/swxstudent.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/swxstudent.css"))

        frag.add_css_url("//stepwise.querium.com/libs/mathquill/mathquill.css")
        frag.add_css_url("//code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css")
        frag.add_css_url("//stepwiseai.querium.com/client/querium-stepwise-1.6.9.css")	

        frag.add_javascript_url("//cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-MML-AM_HTMLorMML")
        frag.add_javascript_url("//stepwise.querium.com/libs/mathquill/mathquill.js")
        frag.add_javascript_url("//ajax.googleapis.com/ajax/libs/angularjs/1.5.3/angular.min.js")
        frag.add_javascript_url("//ajax.googleapis.com/ajax/libs/angularjs/1.5.3/angular-sanitize.min.js")
        frag.add_javascript_url("//ajax.googleapis.com/ajax/libs/angularjs/1.5.3/angular-animate.min.js")
        frag.add_javascript_url("//www.gstatic.com/firebasejs/4.4.0/firebase.js")	# For qEval client-side logging
        frag.add_javascript_url("//stepwiseai.querium.com/client/querium-stepwise-1.6.9.js")	# With start callback


        frag.add_javascript(self.resource_string("static/js/src/swxstudent.js"))
        frag.initialize_js('SWXStudent', data)
        return frag

    # SAVE GRADE
    @XBlock.json_handler
    def save_grade(self, data, suffix=''):
        logger.info('SWXblock save_grade() - entered')
        logger.info("SWXBlock save_grade() - self.max_attempts={a}".format(a=self.max_attempts))

        # Check for missing grading attributes

        logger.info("SWXblock save_grade() initial self={a}".format(a=self))
        logger.info("SWXblock save_grade() initial data={a}".format(a=data))

        try: q_grade_showme_ded = self.q_grade_showme_ded
        except (NameError,AtrributeError) as e:
             logger.info('SWXblock save_grade() - self.q_grade_showme_dev was not defined: {e}'.format(e=e))
             q_grade_showme_ded = -1

        try: q_grade_hints_count = self.q_grade_hints_count
        except (NameError,AtrributeError) as e:
             logger.info('SWXblock save_grade() - self.q_grade_hints_count was not defined: {e}',format(e=e))
             q_grade_hints_count = -1

        try: q_grade_hints_ded = self.q_grade_hints_ded
        except (NameError,AtrributeError) as e:
             logger.info('SWXblock save_grade() - self.q_grade_hints_ded was not defined: {e}'.format(e=e))
             q_grade_hints_ded = -1

        try: q_grade_errors_count = self.q_grade_errors_count
        except (NameError,AtrributeError) as e:
             logger.info('SWXblock save_grade() - self.q_grade_errors_count was not defined: {e}'.format(e=e))
             q_grade_errors_count = -1

        try: q_grade_errors_ded = self.q_grade_errors_ded
        except (NameError,AtrributeError) as e:
             logger.info('SWXblock save_grade() - self.q_grade_errors_ded was not defined: {e}'.format(e=e))
             q_grade_errors_ded = -1

        try: q_grade_min_steps_count = self.q_grade_min_steps_count
        except (NameError,AtrributeError) as e:
             logger.info('SWXblock save_grade() - self.q_grade_min_steps_count was not defined: {e}'.format(e=e))
             q_grade_min_steps_count = -1

        try: q_grade_min_steps_ded = self.q_grade_min_steps_ded
        except (NameError,AtrributeError) as e:
             logger.info('SWXblock save_grade() - self.q_grade_min_steps_ded was not defined: {e}'.format(e=e))
             q_grade_min_steps_ded = -1

        # mcdaniel jul-2020: fix indentation error
        try: q_weight = self.q_weight
        except (NameError,AttributeError) as e:
                logger.info('SWXblock save_grade() - self.q_weight was not defined: {e}'.format(e=e))
                q_weight = 1.0
        logger.info('SWXblock save_grade() - self={a}'.format(a=self))
        logger.info('SWXblock save_grade() - q_weight={a}'.format(a=q_weight))

        # Grading defaults

        if q_grade_showme_ded == -1:
            logger.info('SWXblock save_grade() - showme default set to 3.0')
            q_grade_showme_ded = 3.0
        if q_grade_hints_count == -1:
            logger.info('SWXblock save_grade() - hints_count default set to 2')
            q_grade_hints_count = 2
        if q_grade_hints_ded == -1:
            logger.info('SWXblock save_grade() - hints_ded default set to 1.0')
            q_grade_hints_ded = 1.0
        if q_grade_errors_count == -1:
            logger.info('SWXblock save_grade() - errors_count default set to 3')
            q_grade_errors_count = 3
        if q_grade_errors_ded == -1:
            logger.info('SWXblock save_grade() - errors_ded default set to 1.0')
            q_grade_errors_ded = 1.0
        if q_grade_min_steps_ded == -1:
            logger.info('SWXblock save_grade() - min_steps_ded default set to 0.25')
            q_grade_min_steps_ded = 0.25

        """
        Count the total number of VALID steps the student input.
        Used to determine if they get full credit for entering at least a min number of good steps.
        """
        valid_steps = 0;

        logger.info("SWXblock save_grade() count valid_steps data={d}".format(d=data))
	step_details = data['stepDetails']
        logger.info("SWXblock save_grade() count valid_steps step_details={d}".format(d=step_details))
        logger.info("SWXblock save_grade() count valid_steps len(step_details)={l}".format(l=len(step_details)))
        for c in range(len(step_details)):
            logger.info("SWXblock save_grade() count valid_steps begin examine step c={c} step_details[c]={d}".format(c=c,d=step_details[c]))
            for i in range (len(step_details[c]['info'])):
                logger.info("SWXblock save_grade() count valid_steps examine step c={c} i={i} step_details[c]['info']={s}".format(c=c,i=i,s=step_details[c]['info']))
                logger.info("SWXblock save_grade() count valid_steps examine step c={c} i={i} step_details[c]['info'][i]={s}".format(c=c,i=i,s=step_details[c]['info'][i]))
                step_status = step_details[c]['info'][i]['status']
                if (step_status == 0):       # victory
                    valid_steps += 1
                    logger.info("SWXblock save_grade() count valid_steps c={c} i={i} victory step found".format(c=c,i=i))
                elif (step_status == 1):     # valid step
                    valid_steps += 1
                    logger.info("SWXblock save_grade() count valid_steps c={c} i={i} valid step found".format(c=c,i=i))
                elif (step_status == 3):     # invalid step
                    valid_steps += 0         # don't count invalid steps
                else:
                    logger.info("SWXblock save_grade() count valid_steps c={c} i={i} ignoring step_status={s}".format(c=c,i=i,s=step_status))
                logger.info("SWXblock save_grade() count valid_steps examine step c={c} i={i} step_status={s} valid_steps={v}".format(c=c,i=i,s=step_status,v=valid_steps))
        logger.info("SWXblock save_grade() final valid_steps={v}".format(v=valid_steps))

        grade=3.0
	max_grade=grade

        logger.info('SWXblock save_grade() - initial grade={a} errors={b} errors_count={c} hints={d} hints_count={e} showme={f} min_steps={g} valid_steps={h}'.format(a=grade,b=data['errors'],c=q_grade_errors_count,d=data['hints'],e=q_grade_hints_count,f=data['usedShowMe'],g=q_grade_min_steps_count,h=valid_steps))
        if data['errors']>q_grade_errors_count:
            grade=grade-q_grade_errors_ded
            logger.info('SWXblock save_grade() - errors test errors_ded={a} grade={b}'.format(a=q_grade_errors_ded,b=grade))
        if data['hints']>q_grade_hints_count:
            grade=grade-q_grade_hints_ded
            logger.info('SWXblock save_grade() - hints test hints_ded={a} grade={b}'.format(a=q_grade_hints_ded,b=grade))
        if data['usedShowMe']:
            grade=grade-q_grade_showme_ded
            logger.info('SWXblock save_grade() - showme test showme_ded={a} grade={b}'.format(a=q_grade_showme_ded,b=grade))
	# fuka july-2020 partial deduction for entering too few intermediate steps
	# TODO: Don't subtract on MatchSpec problems
        if (grade >= max_grade and valid_steps < q_grade_min_steps_count):
            grade=grade-q_grade_min_steps_ded
        if grade<0.0:
            logger.info('SWXblock save_grade() - zero negative grade')
            grade=0.0

        logger.info("SWXblock save_grade() final grade={a} q_weight={b}".format(a=grade,b=q_weight))

        self.runtime.publish(self, 'grade',
            {   'value': (grade/3.0)*q_weight,
                'max_value': 1.0*q_weight
            })

        self.solution = data
        self.grade = grade
        # Don't increment attempts on save grade.  We want to increment them when the student starts
        # a question, not when they finish.  Otherwise people can start the question as many times
        # as they want as long as they don't finish it, then reload the page.
        # self.count_attempts += 1
        logger.info("SWXblock save_grade() final self={a}".format(a=self))
        logger.info("SWXblock save_grade() final self.count_attempts={a}".format(a=self.count_attempts))
        logger.info("SWXblock save_grade() final self.solution={a}".format(a=self.solution))
        logger.info("SWXblock save_grade() final self.grade={a}".format(a=self.grade))


    # START ATTEMPT
    @XBlock.json_handler
    def start_attempt(self, data, suffix=''):
        logger.info("SWXblock start_attempt() - entered")
        logger.info("SWXBlock start_attempt() - self.count_attempts={c} max_attempts={m}".format(c=self.count_attempts,m=self.max_attempts))
        self.count_attempts += 1
        logger.info("SWXBlock start_attempt() - updated self.count_attempts={c}".format(c=self.count_attempts))
        logger.info("SWXBlock start_attempt() - done")


    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        logger.info('SWXblock workbench_scenarios() - entered')
        """A canned scenario for display in the workbench."""
        return [
            ("SWXBlock",
             """<swxblock/>
             """),
            ("Multiple SWXBlock",
             """<vertical_demo>
                <swxblock/>
                <swxblock/>
                <swxblock/>
                </vertical_demo>
             """),
        ]


    def studio_view(self, context=None):
        logger.info('SWXblock studio_view() - entered')
        """
        The STUDIO view of the SWXBlock, shown to instructors
        when authoring courses.
        """
        html = self.resource_string("static/html/swxstudio.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/swxstudio.css"))
        frag.add_javascript(self.resource_string("static/js/src/swxstudio.js"))

        frag.initialize_js('SWxStudio')
        return frag

    def author_view(self, context=None):
        logger.info('SWXblock author_view() - entered')
        """
        The AUTHOR view of the SWXBlock, shown to instructors
        when previewing courses.
        """
        html = self.resource_string("static/html/swxauthor.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/swxauthor.css"))
        frag.add_javascript_url("//cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-MML-AM_HTMLorMML")
        frag.add_javascript(self.resource_string("static/js/src/swxauthor.js"))

	logger.info("swxblock SwXAuthor author_view v={a}".format(a=self.q_definition))
	logger.info("swxblock SwXAuthor author_view v1={a} v2={b} v3={c}".format(a=self.q1_definition,b=self.q2_definition,c=self.q3_definition))
	logger.info("swxblock SwXAuthor author_view v4={a} v5={b} v6={c}".format(a=self.q4_definition,b=self.q5_definition,c=self.q6_definition))
	logger.info("swxblock SwXAuthor author_view v7={a} v8={b} v9={c}".format(a=self.q7_definition,b=self.q8_definition,c=self.q9_definition))

        # tell author_view how many variants are defined
        if len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0 and len(self.q3_definition)>0 and len(self.q4_definition)>0 and len(self.q5_definition)>0 and len(self.q6_definition)>0 and len(self.q7_definition)>0 and len(self.q8_definition)>0 and len(self.q9_definition)>0:
            variants = 10
        elif len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0 and len(self.q3_definition)>0 and len(self.q4_definition)>0 and len(self.q5_definition)>0 and len(self.q6_definition)>0 and len(self.q7_definition)>0 and len(self.q8_definition)>0:
            variants = 9
        elif len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0 and len(self.q3_definition)>0 and len(self.q4_definition)>0 and len(self.q5_definition)>0 and len(self.q6_definition)>0 and len(self.q7_definition)>0:
            variants = 8
        elif len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0 and len(self.q3_definition)>0 and len(self.q4_definition)>0 and len(self.q5_definition)>0 and len(self.q6_definition)>0:
            variants = 7
        elif len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0 and len(self.q3_definition)>0 and len(self.q4_definition)>0 and len(self.q5_definition)>0:
            variants = 6
        elif len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0 and len(self.q3_definition)>0 and len(self.q4_definition)>0:
            variants = 5
        elif len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0 and len(self.q3_definition)>0:
            variants = 4
        elif len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0:
            variants = 3
        elif len(self.q_definition)>0 and len(self.q1_definition)>0:
            variants = 2
        else:
            variants = 1

	logger.info("swxblock SwXAuthor author_view variants={a}".format(a=variants))

        frag.initialize_js('SWxAuthor', variants)
        return frag

    # SAVE QUESTION
    @XBlock.json_handler
    def save_question(self, data, suffix=''):
        logger.info('SWXblock save_question() - entered')
        self.q_max_attempts = int(data['q_max_attempts'])
        self.q_weight = float(data['q_weight'])
        if data['q_option_showme'].lower() == u'true':
            self.q_option_showme = True
        else:
            self.q_option_showme = False
        if data['q_option_hint'].lower() == u'true':
            self.q_option_hint = True
        else:
            self.q_option_hint = False
        self.q_grade_showme_ded = float(data['q_grade_showme_ded'])
        self.q_grade_hints_count = int(data['q_grade_hints_count'])
        self.q_grade_hints_ded = float(data['q_grade_hints_ded'])
        self.q_grade_errors_count = int(data['q_grade_errors_count'])
        self.q_grade_errors_ded = float(data['q_grade_errors_ded'])
        self.q_grade_min_steps_count = int(data['q_grade_min_steps_count'])
        self.q_grade_min_steps_ded = float(data['q_grade_min_steps_ded'])

        self.q_id = data['id']
        self.q_label = data['label']
        self.q_stimulus = data['stimulus']
        self.q_definition = data['definition']
        self.q_type = data['qtype']
        self.q_display_math = data['display_math']
        self.q_hint1 = data['hint1']
        self.q_hint2 = data['hint2']
        self.q_hint3 = data['hint3']

        self.q1_id = data['q1_id']
        self.q1_label = data['q1_label']
        self.q1_stimulus = data['q1_stimulus']
        self.q1_definition = data['q1_definition']
        self.q1_type = data['q1_qtype']
        self.q1_display_math = data['q1_display_math']
        self.q1_hint1 = data['q1_hint1']
        self.q1_hint2 = data['q1_hint2']
        self.q_id = data['id']
        self.q_label = data['label']
        self.q_stimulus = data['stimulus']
        self.q_definition = data['definition']
        self.q_type = data['qtype']
        self.q_display_math = data['display_math']
        self.q_hint1 = data['hint1']
        self.q_hint2 = data['hint2']
        self.q_hint3 = data['hint3']

        self.q1_id = data['q1_id']
        self.q1_label = data['q1_label']
        self.q1_stimulus = data['q1_stimulus']
        self.q1_definition = data['q1_definition']
        self.q1_type = data['q1_qtype']
        self.q1_display_math = data['q1_display_math']
        self.q1_hint1 = data['q1_hint1']
        self.q1_hint2 = data['q1_hint2']
        self.q1_hint3 = data['q1_hint3']

        self.q2_id = data['q2_id']
        self.q2_label = data['q2_label']
        self.q2_stimulus = data['q2_stimulus']
        self.q2_definition = data['q2_definition']
        self.q2_type = data['q2_qtype']
        self.q2_display_math = data['q2_display_math']
        self.q2_hint1 = data['q2_hint1']
        self.q2_hint2 = data['q2_hint2']
        self.q2_hint3 = data['q2_hint3']

        self.q3_id = data['q3_id']
        self.q3_label = data['q3_label']
        self.q3_stimulus = data['q3_stimulus']
        self.q3_definition = data['q3_definition']
        self.q3_type = data['q3_qtype']
        self.q3_display_math = data['q3_display_math']
        self.q3_hint1 = data['q3_hint1']
        self.q3_hint2 = data['q3_hint2']
        self.q3_hint3 = data['q3_hint3']

        self.q4_id = data['q4_id']
        self.q4_label = data['q4_label']
        self.q4_stimulus = data['q4_stimulus']
        self.q4_definition = data['q4_definition']
        self.q4_type = data['q4_qtype']
        self.q4_display_math = data['q4_display_math']
        self.q4_hint1 = data['q4_hint1']
        self.q4_hint2 = data['q4_hint2']
        self.q4_hint3 = data['q4_hint3']

        self.q5_id = data['q5_id']
        self.q5_label = data['q5_label']
        self.q5_stimulus = data['q5_stimulus']
        self.q5_definition = data['q5_definition']
        self.q5_type = data['q5_qtype']
        self.q5_display_math = data['q5_display_math']
        self.q5_hint1 = data['q5_hint1']
        self.q5_hint2 = data['q5_hint2']
        self.q5_hint3 = data['q5_hint3']

        self.q6_id = data['q6_id']
        self.q6_label = data['q6_label']
        self.q6_stimulus = data['q6_stimulus']
        self.q6_definition = data['q6_definition']
        self.q6_type = data['q6_qtype']
        self.q6_display_math = data['q6_display_math']
        self.q6_hint1 = data['q6_hint1']
        self.q6_hint2 = data['q6_hint2']
        self.q6_hint3 = data['q6_hint3']

        self.q7_id = data['q7_id']
        self.q7_label = data['q7_label']
        self.q7_stimulus = data['q7_stimulus']
        self.q7_definition = data['q7_definition']
        self.q7_type = data['q7_qtype']
        self.q7_display_math = data['q7_display_math']
        self.q7_hint1 = data['q7_hint1']
        self.q7_hint2 = data['q7_hint2']
        self.q7_hint3 = data['q7_hint3']

        self.q8_id = data['q8_id']
        self.q8_label = data['q8_label']
        self.q8_stimulus = data['q8_stimulus']
        self.q8_definition = data['q8_definition']
        self.q8_type = data['q8_qtype']
        self.q8_display_math = data['q8_display_math']
        self.q8_hint1 = data['q8_hint1']
        self.q8_hint2 = data['q8_hint2']
        self.q8_hint3 = data['q8_hint3']

        self.q9_id = data['q9_id']
        self.q9_label = data['q9_label']
        self.q9_stimulus = data['q9_stimulus']
        self.q9_definition = data['q9_definition']
        self.q9_type = data['q9_qtype']
        self.q9_display_math = data['q9_display_math']
        self.q9_hint1 = data['q9_hint1']
        self.q9_hint2 = data['q9_hint2']
        self.q9_hint3 = data['q9_hint3']

        if len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0 and len(self.q3_definition)>0 and len(self.q4_definition)>0 and len(self.q5_definition)>0 and len(self.q6_definition)>0 and len(self.q7_definition)>0 and len(self.q8_definition)>0 and len(self.q9_definition)>0:
            self.display_name = "Step-by-Step Dynamic [10]"
        elif len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0 and len(self.q3_definition)>0 and len(self.q4_definition)>0 and len(self.q5_definition)>0 and len(self.q6_definition)>0 and len(self.q7_definition)>0 and len(self.q8_definition)>0:
            self.display_name = "Step-by-Step Dynamic [9]"
        elif len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0 and len(self.q3_definition)>0 and len(self.q4_definition)>0 and len(self.q5_definition)>0 and len(self.q6_definition)>0 and len(self.q7_definition)>0:
            self.display_name = "Step-by-Step Dynamic [8]"
        elif len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0 and len(self.q3_definition)>0 and len(self.q4_definition)>0 and len(self.q5_definition)>0 and len(self.q6_definition)>0:
            self.display_name = "Step-by-Step Dynamic [7]"
        elif len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0 and len(self.q3_definition)>0 and len(self.q4_definition)>0 and len(self.q5_definition)>0:
            self.display_name = "Step-by-Step Dynamic [6]"
        elif len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0 and len(self.q3_definition)>0 and len(self.q4_definition)>0:
            self.display_name = "Step-by-Step Dynamic [5]"
        elif len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0 and len(self.q3_definition)>0:
            self.display_name = "Step-by-Step Dynamic [4]"
        elif len(self.q_definition)>0 and len(self.q1_definition)>0 and len(self.q2_definition)>0:
            self.display_name = "Step-by-Step Dynamic [3]"
        elif len(self.q_definition)>0 and len(self.q1_definition)>0:
            self.display_name = "Step-by-Step Dynamic [2]"
        else:
            self.display_name = "Step-by-Step"

        # mcdaniel jul-2020: fix syntax error in print statement
        print(self.display_name)
        return {'result': 'success'}

    # Do necessary overrides from ScorableXBlockMixin
    def has_submitted_answer(self):
        logger.info('SWXblock has_submitted_answer() - entered')
        """
        Returns True if the problem has been answered by the runtime user.
        """
        logger.info("SWXblock has_submitted_answer() {a}".format(a=self.is_answered))
        return self.is_answered

    def get_score(self):
        logger.info('SWXblock get_score() - entered')
        """
        Return a raw score already persisted on the XBlock.  Should not
        perform new calculations.
        Returns:
            Score(raw_earned=float, raw_possible=float)
        """
        logger.info("SWXblock get_score() earned {e}".format(e=self.raw_earned))
        logger.info("SWXblock get_score() max {m}".format(m=self.max_score()))
        return Score(float(self.raw_earned), float(self.max_score()))

    def set_score(self, score):
        """
        Persist a score to the XBlock.
        The score is a named tuple with a raw_earned attribute and a
        raw_possible attribute, reflecting the raw earned score and the maximum
        raw score the student could have earned respectively.
        Arguments:
            score: Score(raw_earned=float, raw_possible=float)
        Returns:
            None
        """
        logger.info("SWXblock set_score() earned {e}".format(e=score.raw_earned))
        self.raw_earned = score.raw_earned

    def calculate_score(self):
        """
        Calculate a new raw score based on the state of the problem.
        This method should not modify the state of the XBlock.
        Returns:
            Score(raw_earned=float, raw_possible=float)
        """
        logger.info("SWXblock calculate_score() grade {g}".format(g=self.grade))
        logger.info("SWXblock calculate_score() max {m}".format(m=self.max_score))
        return Score(float(self.grade), float(self.max_score()))

    def allows_rescore(self):
        """
        Boolean value: Can this problem be rescored?
        Subtypes may wish to override this if they need conditional support for
        rescoring.
        """
        logger.info("SWXblock allows_rescore() False")
        return False

    def max_score(self):
        """
        Function which returns the max score for an xBlock which emits a score
        https://openedx.atlassian.net/wiki/spaces/AC/pages/161400730/Open+edX+Runtime+XBlock+API#OpenedXRuntimeXBlockAPI-max_score(self):
        :return: Max Score for this problem
        """
        # Want the normalized, unweighted score here (1), not the points possible (3)
        return 1

    def weighted_grade(self):
        """
        Returns the block's current saved grade multiplied by the block's
        weight- the number of points earned by the learner.
        """
        logger.info("SWXblock weighted_grade() earned {e}".format(e=self.raw_earned))
        logger.info("SWXblock weighted_grade() weight {w}".format(w=self.q_weight))
        return self.raw_earned * self.q_weight
