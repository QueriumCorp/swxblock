"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
from xblock.core import XBlock
from xblock.fields import Integer, String, Scope
from xblock.fragment import Fragment


class SWXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # FIELDS
    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )

    label = String(help="Question label", default=None, scope=Scope.content)
    description = String(help="Stimulus", default='Solve for \\(a\\).', scope=Scope.content)
    definition = String(help="Definition", default='SolveFor[5a+4=2a-5,a]', scope=Scope.content)
    qtype = String(help="Type", default='gradeBasicAlgebra', scope=Scope.content)
    mathml = String(help="Display Math", default='\\(5a+4=2a-5\\)', scope=Scope.content)
    hint1 = String(help="First Hint", default='', scope=Scope.content)
    hint2 = String(help="Second Hint", default='', scope=Scope.content)
    hint3 = String(help="Third Hint", default='', scope=Scope.content)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The STUDENT view of the SWXBlock, shown to students
        when viewing courses.
        """
        question = {
            "label" : self.label,
            "description" : self.description,
            "definition" : self.definition,
            "qtype" :  self.qtype,
            "mathml" :  self.mathml,
            "hint1" :  self.hint1,
            "hint2" :  self.hint2,
            "hint3" :  self.hint3
        }

        html = self.resource_string("static/html/swxblock.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/swxblock.css"))

        frag.add_css_url("//stepwiseai.querium.com/client/querium-stepwise-1.6.4.css")
        
        frag.add_javascript_url("//cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-MML-AM_HTMLorMML")
        frag.add_javascript_url("//stepwise.querium.com/libs/mathquill/mathquill.js")
        frag.add_javascript_url("//ajax.googleapis.com/ajax/libs/angularjs/1.5.3/angular.min.js")
        frag.add_javascript_url("//ajax.googleapis.com/ajax/libs/angularjs/1.5.3/angular-sanitize.min.js")
        frag.add_javascript_url("//ajax.googleapis.com/ajax/libs/angularjs/1.5.3/angular-animate.min.js")
        frag.add_javascript_url("//stepwiseai.querium.com/client/querium-stepwise-1.6.4.js")

        frag.add_javascript(self.resource_string("static/js/src/swxblock.js"))
        frag.initialize_js('SWXBlock', question)
        return frag
    # SAVE GRADE
    @XBlock.json_handler
    def save_grade(self, data, suffix=''):
        if data['usedShowMe']:
            grade=0
        elif data['errors']<2 and data['hints']<3:
            grade=1
        elif data['errors']==0 and data['hints']==0:
            grade=3
        else:
            grade=2

        self.runtime.publish(self, 'grade', {'value': grade, 'max_value': 3})

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
    # SAVE QUESTION
    @XBlock.json_handler
    def save_question(self, data, suffix=''):
        self.label = data['label']
        self.description = data['description']
        self.definition = data['definition']
        self.qtype = data['qtype']
        self.mathml = data['mathml']
        self.hint1 = data['hint1']
        self.hint2 = data['hint2']
        self.hint3 = data['hint3']

        # self.runtime.publish(self, 'grade', {'value': grade, 'max_value': 3})

