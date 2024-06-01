/**
 * @id java-kotlin/call-references
 * @name Call
 * @description Method Call
 * @kind problem
 * @problem.severity recommendation
 */

import java

from Call c
select c, c.getEnclosingCallable().getQualifiedName() + " " + c.getCallee().getQualifiedName()