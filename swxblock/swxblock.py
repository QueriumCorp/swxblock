"""TO-DO: Write a stimulus of what this XBlock is."""

import pkg_resources
from xblock.core import XBlock
from xblock.fields import Integer, String, Scope
from xblock.fragment import Fragment
from xblockutils.studio_editable import StudioEditableXBlockMixin

@XBlock.wants('user')
class SWXBlock(StudioEditableXBlockMixin, XBlock):
    """
    TO-DO: document what your XBlock does.
    """
    has_author_view = True # tells the xblock to use the AuthorView
    
    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # FIELDS
    display_name = String(display_name="Display name", default='StepWise', scope=Scope.settings)
    q_label = String(help="Question label", default="", scope=Scope.content)
    q_stimulus = String(help="Stimulus", default='Solve for \\(a\\).', scope=Scope.content)
    q_definition = String(help="Definition", default='SolveFor[5a+4=2a-5,a]', scope=Scope.content)
    q_type = String(help="Type", default='gradeBasicAlgebra', scope=Scope.content)
    q_display_math = String(help="Display Math", default='\\(\\)', scope=Scope.content)
    q_hint1 = String(help="First Hint", default='', scope=Scope.content)
    q_hint2 = String(help="Second Hint", default='', scope=Scope.content)
    q_hint3 = String(help="Third Hint", default='', scope=Scope.content)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The STUDENT view of the SWXBlock, shown to students
        when viewing courses.

        user_service = self.runtime.service(self, 'user')
        xb_user = user_service.get_current_user()
            xb_user.emails[0]
        """
        question = {
            "q_label" : self.q_label,
            "q_stimulus" : self.q_stimulus,
            "q_definition" : self.q_definition,
            "q_type" :  self.q_type,
            "q_display_math" :  self.q_display_math,
            "q_hint1" :  self.q_hint1,
            "q_hint2" :  self.q_hint2,
            "q_hint3" :  self.q_hint3
        }

        html = self.resource_string("static/html/swxstudent.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/swxstudent.css"))

        frag.add_css_url("//stepwise.querium.com/libs/mathquill/mathquill.css")
        frag.add_css_url("//code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css")
        frag.add_css_url("//stepwiseai.querium.com/client/querium-stepwise-1.6.5.css")
        
        frag.add_javascript_url("//cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-MML-AM_HTMLorMML")
        frag.add_javascript_url("//stepwise.querium.com/libs/mathquill/mathquill.js")
        frag.add_javascript_url("//ajax.googleapis.com/ajax/libs/angularjs/1.5.3/angular.min.js")
        frag.add_javascript_url("//ajax.googleapis.com/ajax/libs/angularjs/1.5.3/angular-sanitize.min.js")
        frag.add_javascript_url("//ajax.googleapis.com/ajax/libs/angularjs/1.5.3/angular-animate.min.js")
        frag.add_javascript_url("//stepwiseai.querium.com/client/querium-stepwise-1.6.5.js")

        frag.add_javascript(self.resource_string("static/js/src/swxstudent.js"))
        frag.initialize_js('SWXStudent', question)
        return frag
    # SAVE GRADE
    @XBlock.json_handler
    def save_grade(self, data, suffix=''):
        if data['usedShowMe']:
            grade=0
        elif data['errors']==0 and data['hints']==0:
            grade=3
        elif data['errors']<2 and data['hints']<3:
            grade=2
        else:
            grade=1

        self.runtime.publish(self, 'grade', 
            {   'value': grade, 
                'max_value': 3, 
                'details': data
            })

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
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
        """
        The AUTHOR view of the SWXBlock, shown to instructors
        when previewing courses.
        """
        html = self.resource_string("static/html/swxauthor.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/swxauthor.css"))
        frag.add_javascript_url("//cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-MML-AM_HTMLorMML")
        frag.add_javascript(self.resource_string("static/js/src/swxauthor.js"))

        frag.initialize_js('SWxAuthor')
        return frag
        
    # SAVE QUESTION
    @XBlock.json_handler
    def save_question(self, data, suffix=''):
        self.q_label = data['label']
        self.q_stimulus = data['stimulus']
        self.q_definition = data['definition']
        self.q_type = data['qtype']
        self.q_display_math = data['display_math']
        self.q_hint1 = data['hint1']
        self.q_hint2 = data['hint2']
        self.q_hint3 = data['hint3']
        return {'result': 'success'}

